# ----------------- WATERMARK ----------------- #
"""
 ________  ________ ________     
|\   __  \|\  _____\\   ____\    
\ \  \|\  \ \  \__/\ \  \___|    
 \ \   __  \ \   __\\ \  \       
  \ \  \ \  \ \  \_| \ \  \____  
   \ \__\ \__\ \__\   \ \_______\
    \|__|\|__|\|__|    \|_______|
"""
# ----------------- WATERMARK ----------------- #

import feedparser
import aiohttp


async def get_latest():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.welt.de/feeds/latest.rss") as response:
            data = await response.text()
            feed = feedparser.parse(data)
            last_entry = feed.entries[0]

            title = last_entry.get('title', 'Kein Titel')
            summary = last_entry.get('description', 'Keine Beschreibung')
            published = last_entry.get(
                'published', 'No published date')
            category = last_entry.get('category', 'Keine Kategorie')
            author = last_entry.get('author', 'Unbekannt')
            link = last_entry.get('link', 'https://www.welt.de/')
            image = "static/img/no-image.png"

            if last_entry.get('media_content'):
                for img in last_entry.get('media_content'):
                    try:
                        image = img.get('url', 'static/img/no-image.png')
                    except:
                        image = "static/img/no-image.png"
            else:
                image = "static/img/no-image.png"

            return {
                'title': title,
                'summary': summary,
                'published': published,
                'category': category,
                'author': author,
                'link': link,
                'image': image
            }
