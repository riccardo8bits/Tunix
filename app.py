from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from models import local_session, Musica, Base, engine

# cria o banco se não existir
Base.metadata.create_all(engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ricardo007'


# Página inicial
@app.route('/')
def pagina_inicial():
    return render_template('base.html')


# Listar músicas (com filtro opcional por ID)
@app.route('/musicas')
def listar_musicas():
    db_session = local_session()
    termo = request.args.get('id')  # filtro opcional por id
    try:
        sql = select(Musica)
        if termo:
            sql = sql.where(Musica.id == int(termo))
        musicas = db_session.execute(sql).scalars().all()
        return render_template('listar_musicas.html', musicas=musicas, termo=termo)
    except SQLAlchemyError as e:
        print(f'Erro ao consultar músicas: {e}')
        flash('Erro ao carregar músicas', 'error')
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

        if not nome or not artista:
            flash('Nome e artista são obrigatórios!', 'error')
            return redirect(url_for('adicionar_musica'))

        db_session = local_session()
        try:
            nova = Musica(nome=nome, artista=artista, album=album, ano_lancamento=ano)
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


# Deletar música
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



if __name__ == '__main__':
    app.run(debug=True)
