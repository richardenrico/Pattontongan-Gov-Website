from app import app
from app.models import Article, News, Profile, User
from flask import render_template, request, url_for, redirect, session
from flask_paginate import Pagination, get_page_parameter


@app.route('/', methods=['GET', 'POST'])
def home():
    news = News.objects().order_by('-posted_at')[:4]
    announcement = Article.objects(category='pengumuman').order_by('-posted_at').first()
    return render_template('layout.html', news=news, announcement=announcement)

@app.route("/berita")
def news():
    return render_template("news.html")

@app.route('/berita/<slug>', methods=['GET', 'POST'])
def detail(slug):
    news = News.objects(slug=slug).first()
    another_news = News.objects(id__nin=[news.id]).order_by('-posted_at')[:3]
    
    return render_template('post.html', data=news, another_news=another_news)

@app.route('/input/berita', methods=['GET', 'POST'])
def input_news():
    if 'username' in session:
        news = News.objects()
        return render_template('input_forms.html', data=news, endpoint='berita')
    return redirect(url_for('login'))

@app.route('/input/artikel', methods=['GET', 'POST'])
def input_article():
    if 'username' in session:
        article = Article.objects()
        return render_template('input_forms.html', data=article, endpoint='artikel')
    return redirect(url_for('login'))

@app.route('/save/berita', methods=['GET', 'POST'])
def save_news():
    if 'username' in session:
        news = News(title=request.form['title'])
        news.cover = request.form['cover']
        news.content = request.form['content']
        news.slug = '-'.join(request.form['title'].strip().lower().split(' '))
        
        news.save()
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/save/artikel', methods=['GET', 'POST'])
def save_article():
    if 'username' in session:
        article = Article(title=request.form['title'])
        article.cover = request.form['cover']
        article.content = request.form['content']
        article.category = request.form['category']
        
        article.save()
        return redirect(url_for('home'))
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