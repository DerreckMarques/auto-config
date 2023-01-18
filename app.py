import datetime
import sqlite3
from flask import Flask, render_template, abort,  request, url_for, flash, redirect
#auto-config
import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

#
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


#
@app.route('/conf/<int:id>', methods=('GET', 'POST'))
def configurar_id(id):
    if request.method == 'POST':
        host = request.form['host']
        user = request.form['user']
        password = request.form['password']

        if not host:
            flash('Host is required!')
        elif not user:
            flash('User is required!')
        elif not password:
            flash('password is required!')
        else:
            mensagem = conectar(host, user, password)
            flash('"{}"'.format(mensagem))
            #Configurar conexão

    
    post = get_post(id)
    return render_template('configurar_id.html', post=post)

#
@app.route('/configurar', methods=('GET', 'POST'))
def configurar():
    if request.method == 'POST':
        host = request.form['host']
        user = request.form['user']
        password = request.form['password']

        if not host:
            flash('Host is required!')
        elif not user:
            flash('User is required!')
        elif not password:
            flash('password is required!')
        else:
            mensagem = conectar(host, user, password)
            flash('"{}"'.format(mensagem))
            #Configurar conexão
 
    return render_template('configurar.html')

#
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
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
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

#
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

#
@app.route('/cadastrar', methods=('GET', 'POST'))
def cadastrar():
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


#
def conectar(host, user, password):
    dev = Device(host=host, user=user, passwd=password)
    try:
        dev.open()
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        sys.exit(1)
    except Exception as err:
        print (err)
        sys.exit(1)

    with Config(dev, mode='private') as cu:  
        cu.load('set system services netconf traceoptions file test.log', format='set')
        mensagem = cu.pdiff()
        cu.commit(cu.confirm(10))

    mensagem = dev.facts
    dev.close()
    return mensagem

#
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post