from flask import Flask, render_template, request, redirect, session, flash,url_for


class Jogo:
    def __init__(self,nome,categoria,console,nota):
        self.nome = nome
        self.categoria = categoria
        self.console = console
        self.nota = nota

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

adm = Usuario("admin","admin","admin")
usuarios = {adm.nickname : adm}

jogo1 = Jogo('Tetris', "Puzzle", "Atari", 4)
jogo2 = Jogo("Bom da Guerra", "Rack'n Slash", "PS2", 5)
jogo3 = Jogo("Mortal Kombat", "Luta", "PS2",6)
lista = [jogo1, jogo2, jogo3]

app = Flask(__name__)
app.secret_key = "123"

@app.route('/')
def index():
    return render_template('lista.html',titulo="Jogos",jogos = lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash("Faça o login antes de cadastrar um novo jogo")
        return redirect(url_for('login',proxima=url_for('novo')))
    return render_template('novo.html',titulo="Novo Jogo")

@app.route('/criar', methods = ['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    nota = request.form['nota']
    jogo = Jogo(nome,categoria,console,nota)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route("/autenticar",methods=["POST",])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash("Dados incorretos,tente novamente!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session['usuario_logado'] = None
    flash("Usuario deslogado com sucesso!")
    return redirect(url_for('index'))

app.run(port=8080,debug=True)
