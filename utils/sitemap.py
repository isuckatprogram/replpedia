import database


def generate_sitemap():
  wikis = database.get_wikis({})
  s = ''

  s += f'<sitemap><loc>https://replpedia.jdaniels.me/</loc></sitemap>'
  s += f'<sitemap><loc>https://replpedia.jdaniels.me/wikis</loc></sitemap>'

  for w in wikis:
    s += f'<sitemap><loc>https://replpedia.jdaniels.me/wiki/{w["name"]}</loc></sitemap>'
  f = f'<?xml version="1.0" encoding="UTF-8"?> <sitemapindex xmlns="http://www.google.com/schemas/sitemap/0.84"> {s} </sitemapindex>'
  return f