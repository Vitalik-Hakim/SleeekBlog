import os
from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from flask import send_from_directory
from os import listdir
from os.path import isfile, join






def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE title = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
def num_of_uploads():
     list_of_files = os.listdir("/photos")
    if files in list_of_files:
        file1 = open(files,"r")
        verify = file1.read().splitlines()
    
app = Flask(__name__)

app.config['SECRET_KEY'] = 'your secret key'
app.config["IMAGE_UPLOADS"] = "uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/<post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)



@app.route('/')
def index():
    #image = get_post(id)
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    images = conn.execute('SELECT * FROM images').fetchall()
    #conn.execute('SELECT * FROM images WHERE id = 1', (id,))
    conn.close()
    #response = make_response('Any thing...')
    #resp.set_cookie('name', 'value')
    return render_template('index.html', posts=posts, images=images)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/post_image', methods=('GET', 'POST'))
def create_photo():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['link']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO images (title, link) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create_photo.html')

@app.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE title = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE title = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


@app.route("/post_photo")
def post_photo():
    return render_template("post_photo.html")

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            #image.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
        return redirect(url_for('show'))
    return redirect(url_for('index'))

@app.route('/photos')
def show():
    mypath = "uploads"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    return render_template('Gallery.html', onlyfiles=onlyfiles, post=post)



@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)  

# Can change port if you want
app.run(host = '0.0.0.0', port = 5000)
