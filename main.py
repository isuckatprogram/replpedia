from flask import *
import database
import markdown2
import json as j
import time
import sys
from flask_minify import minify
import requests
import os
import urllib.parse
from utils import search

app = Flask('Replpedia')
minify(app=app, html=True, js=True, cssless=True)

# For development only
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
  return render_template('server_error.html'), 500

@app.route('/',methods=['GET','POST'])
def home():
  return render_template('base.html')

@app.route('/create',methods=['GET','POST'])
def create():
  if request.method == 'GET':
    if request.headers['x-replit-user-id'] == '' or request.headers['x-replit-user-id'] == None:
      return render_template('login.html',url='/create')
    return render_template('create.html',username=request.headers['x-replit-user-name'])
  else:
    if request.form['g-recaptcha-response'] == None:
      return "Invalid Captcha"
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
      'secret': os.getenv('RECAPTCHA'),
      'response': request.form['g-recaptcha-response']
    })

    response = r.json()

    if response['success'] == False:
      print(response)
      return "Captcha Error"

    a = database.get_wiki({"name": request.form['name'].lower()})
    content = request.form['content']
    content = content.replace('<','',sys.maxsize).replace('>','',sys.maxsize)
    if a != None:
      return "Another post with the same title already exists"
    html = markdown2.markdown(content)
    database.add_wiki({
      "name": request.form['name'].lower(),
      "content": content,
      "author": request.form['author'],
      "html":html,
      "hidden":False
    })
    return redirect(f'/wiki/{request.form["name"]}')

@app.route('/wiki/<string:name>',methods=['GET','POST'])
def wiki(name):
  admin = False
  
  info = database.get_wiki({"name": name.lower()})
  if info == None:
    return render_template('404.html')
  if request.headers['x-replit-user-name'] == 'PDanielY' or request.headers['x-replit-user-name'] == info['name']:
    admin = True
  if admin == True:
    return render_template('base.html',article_name=info['name'],article_content=info['html'],article_author=info['author'],admin=admin)
  else:
    if info['hidden'] == True:
      return render_template('404.html')
    return render_template('base.html',article_name=info['name'],article_content=info['html'],article_author=info['author'])

@app.route('/search',methods=['GET','POST'])
def search_page():
  if request.method == 'POST':
    json = request.json
    if json['search'] == None:
      return "Missing arguments"
    results_array = search.search(json['search'])
    return j.dumps(results_array)
  else:
    if request.args.get('search') == None:
      return "Missing arguments"
    results = search.search(request.args.get('search'))
    if len(results) == 0:
      return render_template('wiki.html',wikis=[])
    results_array = []
    for i in results:
      if i['hidden'] == True:
        continue
      else:
        results_array.append(i)
    return render_template('wiki.html',wikis=results_array)


@app.route('/ping',methods=['GET','POST'])
def ping():
  return "Pong"

# Admin commands
@app.route('/delete',methods=['GET','POST'])
def delete():
  referrer = request.referrer
  if referrer == None:
    return "Error"
  referrer = referrer.replace('https://','',1).replace('http://','',1)
  name = referrer.split('/')[2]
  name = urllib.parse.unquote(name)
  owner = database.get_wiki({"name": name.lower()})['author']
  if request.headers['x-replit-user-name'] != owner and request.headers['x-replit-user-name'] != "PDanielY":
    return "Error"
  database.delete({"name": name.lower(), "author":owner})
  return redirect('/')

@app.route('/edit',methods=['GET','POST'])
def edit():
  if request.method == 'GET':
    referrer = request.referrer
    if referrer == None:
      return "Error"
    referrer = referrer.replace('https://','',1).replace('http://','',1)
    name = referrer.split('/')[2]

    name = urllib.parse.unquote(name)

    info = database.get_wiki({"name": name.lower()})
    if info == None:
      return "Wiki not found"
    owner = info['author']
    if request.headers['x-replit-user-name'] != owner:
      return "Error"
    return render_template('edit.html',name=info['name'],content=info['content'],username=info['author'])
  elif request.method == 'POST':

    print(request.form)

    name = request.form['name']

    c = request.form['content']
    
    wiki = database.get_wiki({ "name": name.lower()})

    if wiki == None:
      return "Invalid Wiki"
    owner = wiki['author']
    if request.headers['x-replit-user-name'] != owner and request.headers['x-replit-user-name'] != "PDanielY":
      return "Error"

    html = c.replace('<','',sys.maxsize).replace('>','',sys.maxsize)
    
    html = markdown2.markdown(html)
    database.update({ "name": name.lower()}, { 'content': c, 'html': html})

    return redirect('/')

@app.route('/hide',methods=['GET','POST'])
def hide():
  referrer = request.referrer
  if referrer == None:
    return "Error"
  referrer = referrer.replace('https://','',1).replace('http://','',1)
  name = referrer.split('/')[2]

  name = urllib.parse.unquote(name)
  new = database.get_wiki({'name': name})

  if new == None:
    return "No wiki found"
  
  owner = new['author']
  if request.headers['x-replit-user-name'] != owner and request.headers['x-replit-user-name'] != "PDanielY":
    return "Error"

  new['hidden'] = True
  database.update(database.get_wiki({"name": name}),new)
  return 'Done!'

@app.route('/wikis')
def wikis():
  admin = False
  array = []

  if request.headers['x-replit-user-name'] == 'PDanielY':
    admin = True
  
  wikis = database.get_wikis({})
  for i in wikis:
    if i['hidden'] == True and admin == False:
      continue
    else:
      array.append(i)
  return render_template('wiki.html',wikis=array)

app.run(host="0.0.0.0",port=8080)