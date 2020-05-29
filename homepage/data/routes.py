from flask import Flask, render_template, Blueprint
from homepage.data import nyt
from homepage.data.utils import get_news

data = Blueprint('data', __name__)

@data.route('/news')
def news():
    trending_stories = get_news()[0:20]
    return render_template('news.html', title="News", trending_stories=trending_stories)

