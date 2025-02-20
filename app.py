from flask import Flask, render_template
from flask_cors import CORS
from banco_de_dados_uc2 import app as api_app
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Registrando as rotas da API
app.register_blueprint(api_app)

@app.route('/')
def index():
    return render_template('home.html')

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