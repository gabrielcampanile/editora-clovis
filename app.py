from flask import Flask, render_template
from banco_de_dados_uc2 import app as api_app

app = Flask(__name__)

# Registrando as rotas da API
app.register_blueprint(api_app)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/pessoas')
def pessoas():
    return render_template('pessoas.html')

@app.route('/autores')
def autores():
    return render_template('autores.html')

@app.route('/revisores')
def revisores():
    return render_template('revisores.html')

@app.route('/livros')
def livros():
    return render_template('livros.html')

if __name__ == '__main__':
    app.run(debug=True) 