from unicodedata import category
from app import app
from app.models import Article, Profile, User
from flask import render_template, request, url_for, redirect, session
from flask_paginate import Pagination, get_page_parameter

import datetime


@app.route('/', methods=['GET', 'POST'])
def home():
    news = Article.objects(category='berita').order_by('-posted_at')[:4]
    announcement = Article.objects(category='pengumuman').order_by('-posted_at').first()
    return render_template('layout.html', news=news, announcement=announcement)

@app.route("/berita")
def news():
    carousels = Article.objects(category="berita").order_by('-posted_at')[:4]

    news = Article.objects(category="berita").order_by('-posted_at')

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 6

    offset = (page-1) * per_page

    if len(news) < offset:
        return redirect('/error')

    paginated_news = news[offset:offset + per_page]
    pagination = Pagination(page=page, total=len(news), per_page=per_page)
    return render_template("news.html", carousels=carousels, news=paginated_news, pagination=pagination)

@app.route('/<endpoint>/<slug>', methods=['GET', 'POST'])
def detail(endpoint, slug):
    news = Article.objects(category=endpoint, slug=slug).first()
    another_news = Article.objects(id__nin=[news.id], category='berita').order_by('-posted_at')[:3]
    
    return render_template('post.html', data=news, another_news=another_news)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    return render_template('dashboard.html')

@app.route('/dashboard/<endpoint>', methods=['GET', 'POST'])
def view(endpoint):
    article = Article.objects(category=endpoint).order_by('-posted_at')
    return render_template('dashboard.html', data=article, endpoint=endpoint)

@app.route('/input/<endpoint>', methods=['GET', 'POST'])
def input(endpoint):
    if 'username' in session:
        article = Article.objects()
        return render_template('input_forms.html', data=article, endpoint=endpoint)
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    news_count = Article.objects(category='berita').count()
    announcement_count = Article.objects(category='pengumuman').count()
    destination_count = Article.objects(category='wisata').count()
    user_count = User.objects().count()

    return render_template(
        'screens/admin/dashboard.html',
        news_count=news_count,
        announcement_count=announcement_count,
        destination_count=destination_count,
        user_count=user_count
        )

@app.route('/save/<endpoint>', methods=['GET', 'POST'])
def save(endpoint):
    if 'username' in session:
        object_id = request.form['id']
        
        if object_id:
            article = Article.objects(id=object_id).first()
            article.update(
                title = request.form['title'],
                cover = request.form['cover'],
                content = request.form['content'],
                slug = '-'.join(request.form['title'].strip().lower().split(' ')),
                updated_at = datetime.datetime.utcnow()
            )
        else:
            author = User.objects(username = session.get('username')).first()
            
            article = Article(title=request.form['title'])
            article.author = author.name
            article.cover = request.form['cover']
            article.content = request.form['content']
            article.slug = '-'.join(request.form['title'].strip().lower().split(' '))
            article.category = endpoint
            
            article.save()
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/edit/<endpoint>/<article_id>', methods=['GET', 'POST'])
def edit(article_id, endpoint):
    if 'username' in session:
        article = Article.objects(id=article_id).first()
        return render_template('input_forms.html', data=article, endpoint=endpoint)
    return redirect(url_for('login'))

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    Article.objects(id=request.form['id']).delete()
    return redirect(url_for('dashboard'))

@app.route('/login')
def login():
	if 'username' in session:
		return redirect(url_for('home'))
	return render_template('login_form.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    user = User.objects(username=request.form['username'], password=request.form['password']).first()
    password = user.password
    
    if user:
        if(request.form['password'] == password):
            session['username'] = request.form['username']
            return redirect(url_for('login'))

    return 'Invalid username/password'

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))