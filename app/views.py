import datetime
from unicodedata import category
from app import app
from app.models import Announcement, Article, News, Profile, User
from flask import render_template, request, url_for, redirect
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
    # user = User
    news = News.objects()
    return render_template('input_forms.html', data=news, endpoint='berita')

@app.route('/input/artikel', methods=['GET', 'POST'])
def input_article():
    article = Article.objects()
    return render_template('input_forms.html', data=article, endpoint='artikel')

@app.route('/save/berita', methods=['GET', 'POST'])
def save_news():
    news = News(title=request.form['title'])
    news.cover = request.form['cover']
    news.content = request.form['content']
    news.slug = '-'.join(request.form['title'].strip().lower().split(' '))
    
    news.save()
    return redirect(url_for('home'))

@app.route('/save/artikel', methods=['GET', 'POST'])
def save_article():
    article = Article(title=request.form['title'])
    article.cover = request.form['cover']
    article.content = request.form['content']
    article.category = request.form['category']
    
    article.save()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)