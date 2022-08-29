from unicodedata import category
from app import app
from app.models import Article, Profile, User
from flask import render_template, request, url_for, redirect, session
from flask_paginate import Pagination, get_page_parameter

import datetime


@app.route('/', methods=['GET', 'POST'])
def home():
    maps = Article.objects(category='peta').order_by('title')
    news = Article.objects(category='berita').order_by('-posted_at')[:4]
    announcement = Article.objects(category='pengumuman').order_by('-posted_at').first()
    return render_template('layout.html', news=news, announcement=announcement, maps=maps)

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
    if 'username' in session :
        user = User.objects(username = session.get('username')).first()
        return render_template('dashboard.html', role=user.role)
    return redirect(url_for('login'))

@app.route('/dashboard/<endpoint>', methods=['GET', 'POST'])
def view(endpoint):
    if 'username' in session:
        user_role = User.objects(username = session.get('username')).first().role
        if user_role == 'Admin':
            user = User.objects().order_by('name')
            return render_template('dashboard.html', user=user, role=user_role, endpoint=endpoint)
        else:    
            article = Article.objects(category=endpoint).order_by('-posted_at')
            return render_template('dashboard.html', data=article, endpoint=endpoint)
    return redirect(url_for('login'))

@app.route('/input/<endpoint>', methods=['GET', 'POST'])
def input(endpoint):
    if 'username' in session:
        isAdmin = User.objects(username=session.get('username')).first()
        if endpoint == 'user':
            if isAdmin.role == 'Admin':
                user = User.objects()
                return render_template('input_forms.html', user=user, role=isAdmin.role, endpoint=endpoint)
            else:
                return 'No Access'
        else:
            article = Article.objects()
            return render_template('input_forms.html', data=article, endpoint=endpoint)
    return redirect(url_for('login'))

@app.route('/save/<endpoint>', methods=['GET', 'POST'])
def save(endpoint):
    if 'username' in session:
        user_role = User.objects(username = session.get('username')).first()
        object_id = request.form['id']
        
        if object_id:
            if endpoint == 'user':
                if user_role.role == 'Admin':
                    user = User.objects(id=object_id).first()
                    user.update(
                        username = request.form['username'],
                        name = request.form['name'],
                        password = request.form['password']
                    )
                else:
                    return 'No Access'
            else:
                article = Article.objects(id=object_id).first()
                article.update(
                    title = request.form['title'],
                    cover = request.form['cover'],
                    content = request.form['content'],
                    slug = '-'.join(request.form['title'].strip().lower().split(' ')),
                    updated_at = datetime.datetime.utcnow()
                )
        else:
            if endpoint == 'user':
                if user_role.role == 'Admin':
                    user = User(username=request.form['username'])
                    user.name = request.form['name']
                    user.password = request.form['password']
                    user.role = request.form['role']
                    
                    user.save()
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

@app.route('/edit/<endpoint>/<id>', methods=['GET', 'POST'])
def edit(id, endpoint):
    role = User.objects(username=session.get('username')).first().role
    if 'username' in session:
        if endpoint == 'user':
            if role == 'Admin':
                user = User.objects(id=id).first()
                return render_template('input_forms.html', user=user, endpoint=endpoint)
        else:
            article = Article.objects(id=id).first()
            return render_template('input_forms.html', data=article, endpoint=endpoint)
    return redirect(url_for('login'))

@app.route('/delete/<endpoint>', methods=['GET', 'POST'])
def delete(endpoint):
    role = User.objects(username=session.get('username')).first().role
    if 'username' in session:
        if endpoint == 'user':
            if role == 'Admin':
                User.objects(id=request.form['id']).delete()
            else:
                return 'No Access'
        else:
            Article.objects(id=request.form['id']).delete()
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

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