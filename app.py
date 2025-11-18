from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from models import local_session, Musica, Base, engine, Artista

# garante que o banco e tabela existem
Base.metadata.create_all(engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ricardo007'


# Página inicial
@app.route('/')
def pagina_inicial():
    return render_template('base.html')



# Listar músicas
@app.route('/musicas')
def listar_musicas():
    db_session = local_session()
    try:
        sql = select(Musica)
        musicas = db_session.execute(sql).scalars().all()
        return render_template('listar_musicas.html', musicas=musicas)
    except SQLAlchemyError as e:
        print(f'Erro ao consultar músicas: {e}')
        flash('Erro ao carregar músicas', 'error')
        return redirect(url_for('pagina_inicial'))
    except Exception as e:
        db_session.rollback()
        return redirect(url_for('pagina_inicial'))
    finally:
        db_session.close()


# Adicionar nova música
@app.route('/adicionar_musica', methods=['GET', 'POST'])
def adicionar_musica():
    if request.method == 'POST':
        nome = request.form.get('nome')
        artista = request.form.get('artista')
        album = request.form.get('album')
        ano = request.form.get('ano')
        url_img = request.form.get('url_img')

        if not nome or not artista:
            flash('Nome e artista são obrigatórios!', 'error')
            return redirect(url_for('adicionar_musica'))

        db_session = local_session()
        try:
            nova = Musica(nome=nome, artista=artista, album=album, ano_lancamento=ano, url_img=url_img)
            db_session.add(nova)
            db_session.commit()
            flash('Música adicionada com sucesso!', 'success')
            return redirect(url_for('listar_musicas'))
        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Erro ao salvar música!', 'error')
            print(e)
        finally:
            db_session.close()
    return render_template('adicionar_musica.html')


# Ver detalhes de uma música
@app.route('/musica/<int:id_musica>')
def musica_especifica(id_musica):
    db_session = local_session()
    musica = db_session.get(Musica, id_musica)
    db_session.close()
    if not musica:
        flash('Música não encontrada.', 'error')
        return redirect(url_for('listar_musicas'))
    return render_template('musica_especifica.html', musica=musica)


# Excluir música
@app.route('/musica/<int:id_musica>/deletar', methods=['POST'])
def deletar_musica(id_musica):
    db_session = local_session()
    musica = db_session.get(Musica, id_musica)
    if not musica:
        flash('Música não encontrada.', 'error')
        return redirect(url_for('listar_musicas'))
    try:
        db_session.delete(musica)
        db_session.commit()
        flash('Música excluída com sucesso!', 'success')
    except Exception as e:
        db_session.rollback()
        flash('Erro ao excluir música.', 'error')
        print(e)
    finally:
        db_session.close()
    return redirect(url_for('listar_musicas'))
@app.route('/artistas')
def listar_artistas():
    db_session = local_session()
    try:
        sql = select(Artista)
        artistas = db_session.execute(sql).scalars().all()
        return render_template('listar_artistas.html', artistas=artistas)
    except SQLAlchemyError as e:
        print(f'Erro ao consultar artistas: {e}')
        flash('Erro ao carregar artistas', 'error')
        db_session.rollback()
        return redirect(url_for('pagina_inicial'))
    except Exception as e:
        db_session.rollback()
        flash('Erro inesperado', 'error')
        return redirect(url_for('pagina_inicial'))
    finally:
        db_session.close()


# Adicionar nova música
@app.route('/adicionar_artista', methods=['GET', 'POST'])
def adicionar_artista():
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        data_nascimento = request.form.get('data_nascimento')
        url_img = request.form.get('url_img')

        if not nome or not sobrenome:
            flash('Nome e sobrenome são obrigatórios!', 'error')
            return redirect(url_for('adicionar_artista'))

        db_session = local_session()
        try:
            nova = Artista(nome=nome, sobrenome=sobrenome, data_nascimento=data_nascimento, url_img=url_img)
            db_session.add(nova)
            db_session.commit()
            flash('Música adicionado com sucesso!', 'success')
            return redirect(url_for('listar_artistas'))
        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Erro ao salvar artista!', 'error')
            print(e)
        finally:
            db_session.close()
    return render_template('adicionar_artista.html')


# Ver detalhes de uma música
@app.route('/artista/<int:id_artista>')
def artista_especifica(id_artista):
    db_session = local_session()
    artista = db_session.get(Artista, id_artista)
    db_session.close()
    if not Artista:
        flash('Artista não encontrado.', 'error')
        return redirect(url_for('listar_artistas'))
    return render_template('artista_especifica.html', artista=artista)


# Excluir música
@app.route('/artista/<int:id_artista>/deletar', methods=['POST'])
def deletar_artista(id_artista):
    db_session = local_session()
    artista = db_session.get(Artista, id_artista)
    if not artista:
        flash('Artista não encontrada.', 'error')
        return redirect(url_for('listar_artistas'))
    try:
        db_session.delete(artista)
        db_session.commit()
        flash('Artista excluída com sucesso!', 'success')
    except Exception as e:
        db_session.rollback()
        flash('Erro ao excluir artista.', 'error')
        print(e)
    finally:
        db_session.close()
    return redirect(url_for('listar_artistas'))






if __name__ == '__main__':
    app.run(debug=True)
