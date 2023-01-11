import datetime
from flask import Flask, render_template, abort,  request, url_for, flash, redirect
#auto-config
import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

@app.route('/', methods=('POST', 'GET'))
def index():
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


    return render_template('index.html')

@app.route('/cadastrar', methods=('POST', 'GET'))
def create():
    return render_template('create.html')


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

