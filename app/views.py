from unicodedata import category
from app import app
from app.models import Article, Profile, User
from flask import render_template, request, url_for, redirect, session
from flask_paginate import Pagination, get_page_parameter


@app.route('/', methods=['GET', 'POST'])
def home():
    news = Article.objects(category='berita').order_by('-posted_at')[:4]
    announcement = Article.objects(category='pengumuman').order_by('-posted_at').first()
    return render_template('layout.html', news=news, announcement=announcement)

@app.route("/berita")
def news():
    return render_template("news.html")

@app.route('/berita/<slug>', methods=['GET', 'POST'])
def detail(slug):
    news = Article.objects(category='berita', slug=slug).first()
    another_news = Article.objects(id__nin=[news.id], category='berita').order_by('-posted_at')[:3]
    
    return render_template('post.html', data=news, another_news=another_news)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    
    return render_template('dashboard.html')

@app.route('/input/<endpoint>', methods=['GET', 'POST'])
def input(endpoint):
    if 'username' in session:
        article = Article.objects()
        return render_template('input_forms.html', data=article, endpoint=endpoint)
    return redirect(url_for('login'))

@app.route('/save/<endpoint>', methods=['GET', 'POST'])
def save(endpoint):
    if 'username' in session:
        author = User.objects(username = session.get('username')).first()
        
        article = Article(title=request.form['title'])
        article.author = author.name
        article.cover = request.form['cover']
        article.content = request.form['content']
        article.slug = '-'.join(request.form['title'].strip().lower().split(' '))
        article.category = endpoint
        
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