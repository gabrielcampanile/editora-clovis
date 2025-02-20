from flask import Flask, request, jsonify, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from modelos_editoraClovis import Pessoa, Revisor, Autor, Livro, Escreve, Revisa
from config import Config

app = Blueprint('api', __name__)

# Configuração do banco de dados
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

#############################
# PESSOA
#############################

@app.route('/pessoa', methods=['POST'])
def add_pessoa():
    session = Session()
    data = request.get_json()

    nova_pessoa = Pessoa(
        cod_pessoa=data['cod_pessoa'],
        CPF=data['CPF'],
        nome=data['nome'],
        data_nasc=data['data_nasc']
    )
    
    session.add(nova_pessoa)
    session.commit()
    session.close()

    return jsonify({'message': 'Pessoa adicionada com sucesso!'}), 201

@app.route('/pessoa', methods=['GET'])
def get_pessoas():
    session = Session()
    pessoas = session.query(Pessoa).order_by(Pessoa.cod_pessoa).all()
    session.close()

    return jsonify([{
        'cod_pessoa': pessoa.cod_pessoa,
        'CPF': pessoa.CPF,
        'nome': pessoa.nome,
        'data_nasc': pessoa.data_nasc.isoformat()
    } for pessoa in pessoas])

@app.route('/pessoa/<int:cod_pessoa>', methods=['PUT'])
def update_pessoa(cod_pessoa):
    session = Session()
    pessoa = session.query(Pessoa).filter_by(cod_pessoa=cod_pessoa).first()

    if pessoa:
        data = request.get_json()
        pessoa.nome = data['nome']
        session.commit()
        session.close()

        return jsonify({'message': 'Pessoa atualizada com sucesso!'})
    
    session.close()
    return jsonify({'message': 'Pessoa não encontrada!'}), 404

@app.route('/pessoa/<int:cod_pessoa>', methods=['DELETE'])
def delete_pessoa(cod_pessoa):
    session = Session()
    pessoa = session.query(Pessoa).filter_by(cod_pessoa=cod_pessoa).first()

    if pessoa:
        session.delete(pessoa)
        session.commit()
        session.close()
        return jsonify({'message': 'Pessoa excluída com sucesso!'})
    
    session.close()
    return jsonify({'message': 'Pessoa não encontrada!'}), 404

@app.route('/pessoa/<int:cod_pessoa>', methods=['GET'])
def get_pessoa(cod_pessoa):
    session = Session()
    pessoa = session.query(Pessoa).filter_by(cod_pessoa=cod_pessoa).first()
    session.close()
    
    if pessoa:
        return jsonify({
            'cod_pessoa': pessoa.cod_pessoa,
            'CPF': pessoa.CPF,
            'nome': pessoa.nome,
            'data_nasc': pessoa.data_nasc.isoformat()
        })
    return jsonify({'message': 'Pessoa não encontrada'}), 404

#############################
# REVISOR
#############################

@app.route('/revisor', methods=['GET'])
def get_revisores():
    session = Session()
    revisores = session.query(Revisor).order_by(Revisor.cod_revisor).all()
    session.close()
    return jsonify([{
        'cod_revisor': revisor.cod_revisor,
        'cod_pessoa': revisor.cod_pessoa,
        'especialidade': revisor.especialidade,
        'salario': float(revisor.salario),
        'data_contrato': revisor.data_contrato.isoformat()
    } for revisor in revisores])

@app.route('/revisor/<int:cod_revisor>', methods=['GET'])
def get_revisor(cod_revisor):
    session = Session()
    revisor = session.query(Revisor).filter_by(cod_revisor=cod_revisor).first()
    if revisor:
        return jsonify({
            'cod_revisor': revisor.cod_revisor,
            'cod_pessoa': revisor.cod_pessoa,
            'especialidade': revisor.especialidade,
            'salario': float(revisor.salario),
            'data_contrato': revisor.data_contrato.isoformat()
        })
    return jsonify({'message': 'Revisor não encontrado'}), 404

@app.route('/revisor', methods=['POST'])
def add_revisor():
    session = Session()
    data = request.get_json()
    
    novo_revisor = Revisor(
        cod_revisor=data['cod_revisor'],
        cod_pessoa=data['cod_pessoa'],
        especialidade=data['especialidade'],
        salario=data['salario'],
        data_contrato=data['data_contrato']
    )
    
    try:
        session.add(novo_revisor)
        session.commit()
        return jsonify({'message': 'Revisor adicionado com sucesso!'}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@app.route('/revisor/<int:cod_revisor>', methods=['PUT'])
def update_revisor(cod_revisor):
    session = Session()
    data = request.get_json()
    revisor = session.query(Revisor).filter_by(cod_revisor=cod_revisor).first()
    
    if revisor:
        try:
            revisor.cod_pessoa = data['cod_pessoa']
            revisor.especialidade = data['especialidade']
            revisor.salario = data['salario']
            revisor.data_contrato = data['data_contrato']
            session.commit()
            return jsonify({'message': 'Revisor atualizado com sucesso!'})
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
        finally:
            session.close()
    
    session.close()
    return jsonify({'message': 'Revisor não encontrado'}), 404

@app.route('/revisor/<int:cod_revisor>', methods=['DELETE'])
def delete_revisor(cod_revisor):
    session = Session()
    revisor = session.query(Revisor).filter_by(cod_revisor=cod_revisor).first()
    
    if revisor:
        try:
            session.delete(revisor)
            session.commit()
            return jsonify({'message': 'Revisor excluído com sucesso!'})
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
        finally:
            session.close()
    
    session.close()
    return jsonify({'message': 'Revisor não encontrado'}), 404

#############################
# LIVRO
#############################

@app.route('/livro', methods=['GET'])
def get_livros():
    session = Session()
    livros = session.query(Livro).order_by(Livro.cod_livro).all()
    session.close()
    return jsonify([{
        'cod_livro': livro.cod_livro,
        'titulo': livro.titulo,
        'genero': livro.genero
    } for livro in livros])

@app.route('/livro/<int:cod_livro>', methods=['GET'])
def get_livro(cod_livro):
    session = Session()
    livro = session.query(Livro).filter_by(cod_livro=cod_livro).first()
    if livro:
        return jsonify({
            'cod_livro': livro.cod_livro,
            'titulo': livro.titulo,
            'genero': livro.genero
        })
    return jsonify({'message': 'Livro não encontrado'}), 404

@app.route('/livro', methods=['POST'])
def add_livro():
    session = Session()
    data = request.get_json()
    
    novo_livro = Livro(
        cod_livro=data['cod_livro'],
        titulo=data['titulo'],
        genero=data['genero']
    )
    
    try:
        session.add(novo_livro)
        session.commit()
        
        # Adicionar autores
        if 'autores' in data:
            for cod_autor in data['autores']:
                escreve = Escreve(
                    cod_autor=cod_autor,
                    cod_livro=novo_livro.cod_livro,
                    cod_pessoa=session.query(Autor).filter_by(cod_autor=cod_autor).first().cod_pessoa
                )
                session.add(escreve)
        
        # Adicionar revisores
        if 'revisores' in data:
            for cod_revisor in data['revisores']:
                revisa = Revisa(
                    cod_revisor=cod_revisor,
                    cod_livro=novo_livro.cod_livro,
                    cod_pessoa=session.query(Revisor).filter_by(cod_revisor=cod_revisor).first().cod_pessoa,
                    status_revisao='Em andamento'
                )
                session.add(revisa)
        
        session.commit()
        return jsonify({'message': 'Livro adicionado com sucesso!'}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@app.route('/livro/<int:cod_livro>', methods=['PUT'])
def update_livro(cod_livro):
    session = Session()
    data = request.get_json()
    livro = session.query(Livro).filter_by(cod_livro=cod_livro).first()
    
    if livro:
        try:
            livro.titulo = data['titulo']
            livro.genero = data['genero']
            
            # Atualizar autores
            session.query(Escreve).filter_by(cod_livro=cod_livro).delete()
            if 'autores' in data:
                for cod_autor in data['autores']:
                    escreve = Escreve(
                        cod_autor=cod_autor,
                        cod_livro=cod_livro,
                        cod_pessoa=session.query(Autor).filter_by(cod_autor=cod_autor).first().cod_pessoa
                    )
                    session.add(escreve)
            
            # Atualizar revisores
            session.query(Revisa).filter_by(cod_livro=cod_livro).delete()
            if 'revisores' in data:
                for cod_revisor in data['revisores']:
                    revisa = Revisa(
                        cod_revisor=cod_revisor,
                        cod_livro=cod_livro,
                        cod_pessoa=session.query(Revisor).filter_by(cod_revisor=cod_revisor).first().cod_pessoa,
                        status_revisao='Em andamento'
                    )
                    session.add(revisa)
            
            session.commit()
            return jsonify({'message': 'Livro atualizado com sucesso!'})
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
        finally:
            session.close()
    
    session.close()
    return jsonify({'message': 'Livro não encontrado'}), 404

@app.route('/livro/<int:cod_livro>', methods=['DELETE'])
def delete_livro(cod_livro):
    session = Session()
    livro = session.query(Livro).filter_by(cod_livro=cod_livro).first()
    
    if livro:
        try:
            # Remover relacionamentos primeiro
            session.query(Escreve).filter_by(cod_livro=cod_livro).delete()
            session.query(Revisa).filter_by(cod_livro=cod_livro).delete()
            session.delete(livro)
            session.commit()
            return jsonify({'message': 'Livro excluído com sucesso!'})
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 400
        finally:
            session.close()
    
    session.close()
    return jsonify({'message': 'Livro não encontrado'}), 404

@app.route('/livro/<int:cod_livro>/autores', methods=['GET'])
def get_autores_livro(cod_livro):
    session = Session()
    autores = session.query(Autor).join(Escreve).filter(Escreve.cod_livro == cod_livro).all()
    
    result = []
    for autor in autores:
        pessoa = session.query(Pessoa).filter_by(cod_pessoa=autor.cod_pessoa).first()
        result.append({
            'cod_autor': autor.cod_autor,
            'cod_pessoa': autor.cod_pessoa,
            'nome': pessoa.nome if pessoa else 'N/A'
        })
    
    session.close()
    return jsonify(result)

@app.route('/livro/<int:cod_livro>/revisores', methods=['GET'])
def get_revisores_livro(cod_livro):
    session = Session()
    revisores = session.query(Revisor).join(Revisa).filter(Revisa.cod_livro == cod_livro).all()
    
    result = []
    for revisor in revisores:
        pessoa = session.query(Pessoa).filter_by(cod_pessoa=revisor.cod_pessoa).first()
        result.append({
            'cod_revisor': revisor.cod_revisor,
            'cod_pessoa': revisor.cod_pessoa,
            'nome': pessoa.nome if pessoa else 'N/A',
            'especialidade': revisor.especialidade
        })
    
    session.close()
    return jsonify(result)

#############################
# ESCREVE
#############################


# CREATE (Adicionar Escreve)
@app.route('/escreve', methods=['POST'])
def add_escreve():
    session = Session()
    data = request.get_json()
    novo_escreve = Escreve(
        cod_autor=data['cod_autor'],
        cod_pessoa=data['cod_pessoa'],
        cod_livro=data['cod_livro']
    )
    session.add(novo_escreve)
    session.commit()
    return jsonify({'message': 'Registro na tabela Escreve criado com sucesso!'}), 201

# READ (Ler Escreve)
@app.route('/escreve/<int:cod_autor>/<int:cod_pessoa>/<int:cod_livro>', methods=['GET'])
def get_escreve(cod_autor, cod_pessoa, cod_livro):
    session = Session()
    escreves = session.query(Escreve).filter_by(
        cod_autor=cod_autor, cod_pessoa=cod_pessoa, cod_livro=cod_livro).first()
    if escreves:
        return jsonify({
            'cod_autor': escreves.cod_autor,
            'cod_pessoa': escreves.cod_pessoa,
            'cod_livro': escreves.cod_livro
        })
    return jsonify({'message': 'Registro não encontrado'}), 404

# UPDATE (Atualizar Escreve)
@app.route('/escreve/<int:cod_autor>/<int:cod_pessoa>/<int:cod_livro>', methods=['PUT'])
def update_escreve(cod_autor, cod_pessoa, cod_livro):
    session = Session()
    data = request.get_json()
    escreves = session.query(Escreve).filter_by(
        cod_autor=cod_autor, cod_pessoa=cod_pessoa, cod_livro=cod_livro).first()
    if escreves:
        escreves.cod_autor = data['cod_autor']
        escreves.cod_pessoa = data['cod_pessoa']
        escreves.cod_livro = data['cod_livro']
        session.commit()
        return jsonify({'message': 'Registro na tabela Escreve atualizado com sucesso!'})
    return jsonify({'message': 'Registro não encontrado'}), 404

# DELETE (Deletar Escreve)
@app.route('/escreve/<int:cod_autor>/<int:cod_pessoa>/<int:cod_livro>', methods=['DELETE'])
def delete_escreve(cod_autor, cod_pessoa, cod_livro):
    session = Session()
    escreves = session.query(Escreve).filter_by(
        cod_autor=cod_autor, cod_pessoa=cod_pessoa, cod_livro=cod_livro).first()
    if escreves:
        session.delete(escreves)
        session.commit()
        return jsonify({'message': 'Registro na tabela Escreve deletado com sucesso!'})
    return jsonify({'message': 'Registro não encontrado'}), 404


#############################
# REVISA
#############################



# CREATE (Adicionar Revisa)
@app.route('/revisa', methods=['POST'])
def add_revisa():
    session = Session()
    data = request.get_json()
    nova_revisa = Revisa(
        cod_revisor=data['cod_revisor'],
        cod_pessoa=data['cod_pessoa'],
        cod_livro=data['cod_livro'],
        status_revisao=data['status_revisao']
    )
    session.add(nova_revisa)
    session.commit()
    return jsonify({'message': 'Registro na tabela Revisa criado com sucesso!'}), 201

# READ (Ler Revisa)
@app.route('/revisa/<int:cod_revisor>/<int:cod_pessoa>/<int:cod_livro>', methods=['GET'])
def get_revisa(cod_revisor, cod_pessoa, cod_livro):
    session = Session()
    revisa = session.query(Revisa).filter_by(
        cod_revisor=cod_revisor, cod_pessoa=cod_pessoa, cod_livro=cod_livro).first()
    if revisa:
        return jsonify({
            'cod_revisor': revisa.cod_revisor,
            'cod_pessoa': revisa.cod_pessoa,
            'cod_livro': revisa.cod_livro,
            'status_revisao': revisa.status_revisao
        })
    return jsonify({'message': 'Registro não encontrado'}), 404

# UPDATE (Atualizar Revisa)
@app.route('/revisa/<int:cod_revisor>/<int:cod_pessoa>/<int:cod_livro>', methods=['PUT'])
def update_revisa(cod_revisor, cod_pessoa, cod_livro):
    session = Session()
    data = request.get_json()
    revisa = session.query(Revisa).filter_by(
        cod_revisor=cod_revisor, cod_pessoa=cod_pessoa, cod_livro=cod_livro).first()
    if revisa:
        revisa.status_revisao = data['status_revisao']
        session.commit()
        return jsonify({'message': 'Registro na tabela Revisa atualizado com sucesso!'})
    return jsonify({'message': 'Registro não encontrado'}), 404

# DELETE (Deletar Revisa)
@app.route('/revisa/<int:cod_revisor>/<int:cod_pessoa>/<int:cod_livro>', methods=['DELETE'])
def delete_revisa(cod_revisor, cod_pessoa, cod_livro):
    session = Session()
    revisa = session.query(Revisa).filter_by(
        cod_revisor=cod_revisor, cod_pessoa=cod_pessoa, cod_livro=cod_livro).first()
    if revisa:
        session.delete(revisa)
        session.commit()
        return jsonify({'message': 'Registro na tabela Revisa deletado com sucesso!'})
    return jsonify({'message': 'Registro não encontrado'}), 404


#############################
# AUTOR
#############################


# CREATE (Adicionar Autor)
@app.route('/autor', methods=['POST'])
def add_autor():
    session = Session()
    data = request.get_json()
    novo_autor = Autor(
        cod_autor=data['cod_autor'],
        cod_pessoa=data['cod_pessoa']
    )
    session.add(novo_autor)
    session.commit()
    return jsonify({'message': 'Registro na tabela Autor criado com sucesso!'}), 201

# READ (Ler Autor)
@app.route('/autor/<int:cod_autor>/<int:cod_pessoa>', methods=['GET'])
def get_autor(cod_autor, cod_pessoa):
    session = Session()
    autor = session.query(Autor).filter_by(cod_autor=cod_autor, cod_pessoa=cod_pessoa).first()
    if autor:
        return jsonify({
            'cod_autor': autor.cod_autor,
            'cod_pessoa': autor.cod_pessoa
        })
    return jsonify({'message': 'Registro não encontrado'}), 404

# UPDATE (Atualizar Autor)
@app.route('/autor/<int:cod_autor>/<int:cod_pessoa>', methods=['PUT'])
def update_autor(cod_autor, cod_pessoa):
    session = Session()
    data = request.get_json()
    autor = session.query(Autor).filter_by(cod_autor=cod_autor, cod_pessoa=cod_pessoa).first()
    if autor:
        autor.cod_autor = data['cod_autor']
        autor.cod_pessoa = data['cod_pessoa']
        session.commit()
        return jsonify({'message': 'Registro na tabela Autor atualizado com sucesso!'})
    return jsonify({'message': 'Registro não encontrado'}), 404

# DELETE (Deletar Autor)
@app.route('/autor/<int:cod_autor>/<int:cod_pessoa>', methods=['DELETE'])
def delete_autor(cod_autor, cod_pessoa):
    session = Session()
    autor = session.query(Autor).filter_by(cod_autor=cod_autor, cod_pessoa=cod_pessoa).first()
    if autor:
        session.delete(autor)
        session.commit()
        return jsonify({'message': 'Registro na tabela Autor deletado com sucesso!'})
    return jsonify({'message': 'Registro não encontrado'}), 404

@app.route('/autor', methods=['GET'])
def get_autores():
    session = Session()
    autores = session.query(Autor).order_by(Autor.cod_autor).all()
    session.close()
    return jsonify([{
        'cod_autor': autor.cod_autor,
        'cod_pessoa': autor.cod_pessoa
    } for autor in autores])

if __name__ == '__main__':
    app.run(debug=True)