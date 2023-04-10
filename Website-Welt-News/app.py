from quart import Quart, render_template, url_for
from datetime import datetime
from func.news import get_latest

app = Quart(__name__, static_folder='static',
            template_folder='templates')


@app.route('/')
async def _latest():
    news = await get_latest()
    title = news.get('title')
    summary = news.get('summary')
    published = news.get('published')
    category = news.get('category')
    author = news.get('author')
    link = news.get('link')
    img = news.get('image')

    # ---------------------------------- #
    if datetime == "No published date":
        published = datetime.now().strftime('%d.%m.%Y')
    else:
        published = datetime.strptime(published, '%a, %d %b %Y %H:%M:%S %Z')
        published = published.strftime('%d.%m.%Y')
    # ---------------------------------- #

    return await render_template('latest.html', image=img, title=title, summary=summary, published=published, category=category, author=author, post=link)


if __name__ == '__main__':
    app.run(debug=True)
