from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
from models import local_session, Musica, Base, engine, Artista, Albuns, Usuario, Avaliacao
import random

# garante que o banco e tabela existem
Base.metadata.create_all(engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ricardo007'


# Página inicial
@app.route('/')
def pagina_inicial():
    db_session = local_session()

    # Buscar todas as músicas
    sql = (select(Musica.nome, func.count(Avaliacao.id).label("curtidas"))
           .select_from(Avaliacao)
            .join(Musica, Musica.id == Avaliacao.id_musica)
           .group_by(Avaliacao.id_musica, Musica.nome)
           .order_by(func.count(Avaliacao.id).label("curtidas").desc())
           .limit(10))
    musicas = db_session.execute(sql).all()
    print(musicas)


    return render_template('pagina_inicial.html', musicas=musicas)



# Listar músicas
@app.route('/musicas')
def listar_musicas():
    db_session = local_session()
    try:
        sql = select(Musica)
        musicas = db_session.execute(sql).scalars().all()
        # print('jhgg', musicas)
        return render_template('listar_musicas.html', var_musicas=musicas)
    except SQLAlchemyError as e:
        print(f'Erro ao consultar músicas: {e}')
        flash('Erro ao carregar músicas', 'error')
        return redirect(url_for('pagina_inicial'))
    except Exception as e:
        db_session.rollback()
        print(f'Erroxx:  {e}')
        return redirect(url_for('pagina_inicial'))
    finally:
        db_session.close()


# Adicionar nova música
@app.route('/adicionar_musica', methods=['GET', 'POST'])
def adicionar_musica():
    if request.method == 'POST':
        nome_ = request.form.get('nome')
        artista_ = request.form.get('artista')
        album_ = request.form.get('album')
        ano_ = request.form.get('ano')
        letras_ = request.form.get('letras')
        url_img_ = request.form.get('url_img')

        print(nome_, artista_, album_, ano_, letras_, url_img_)

        if not nome_ or not artista_:
            flash('Nome e artista são obrigatórios!', 'error')
            return redirect(url_for('adicionar_musica'))

        db_session = local_session()
        try:
            nova = Musica(nome=nome_, artista=artista_, album=album_, ano_lancamento=ano_, letras=letras_, url_img=url_img_)
            db_session.add(nova)
            db_session.commit()
            flash('Música adicionada com sucesso!', 'success')
            return redirect(url_for('listar_musicas'))
        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Erro ao salvar música!', 'error')
            print(e)
            return redirect(url_for('listar_musicas'))
        except Exception as e:
            db_session.rollback()
            flash('Erro inesperado ao salvar música!', 'error')
            print(e)
            return redirect(url_for('listar_musicas'))
        finally:
            db_session.close()
    return render_template('adicionar_musica.html')


# Ver detalhes de uma música
@app.route('/musica/<int:id_musica>')
def musica_especifica(id_musica):
    db_session = local_session()
    musica = db_session.get(Musica, id_musica)
    sql1 = select(func.count(Avaliacao.id_usuario)).where(Avaliacao.id_musica == int(id_musica))
    avaliacoes = db_session.execute(sql1).scalars().first()
    db_session.close()
    if not musica:
        flash('Música não encontrada.', 'error')
        return redirect(url_for('listar_musicas'))
    return render_template('musica_especifica.html', musica=musica, avaliacoes=avaliacoes)


# Excluir música
@app.route('/musica/<int:id_musica>/deletar', methods=['GET', 'POST'])
def deletar_musica(id_musica):
    db_session = local_session()
    musica_sql = select(Musica).where(Musica.id == id_musica)
    musica = db_session.execute(musica_sql).scalars().one_or_none()
    if not musica:
        flash('Música não encontrada.', 'error')
        db_session.close()
        return redirect(url_for('listar_musicas'))

    try:
        db_session.delete(musica)
        db_session.commit()
        flash('Música excluída com sucesso!', 'success')
        return redirect(url_for('listar_musicas'))
    except Exception as e:
        db_session.rollback()
        print("erro", e)
        flash('Erro ao excluir música.', 'error')
    finally:
        db_session.close()

    return redirect(url_for('listar_musicas'))





@app.route('/artistas')
def listar_artistas():
    db_session = local_session()
    try:
        sql = select(Artista)
        artistas = db_session.execute(sql).scalars().all()
        return render_template('listar_artistas.html', var_artistas=artistas)
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
@app.route('/artista/<int:id_artista>/deletar', methods=['POST', 'GET'])
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


@app.route('/artista/<int:id_artista>/editar_artista', methods=['GET', 'POST'])
def editar_artista(id_artista):
    db_session = local_session()
    artista = db_session.get(Artista, id_artista)

    if not artista:
        flash("Música não encontrada.", "error")
        return redirect(url_for('listar_artistas'))

    if request.method == 'POST':
        artista.nome = request.form.get('nome')
        artista.sobrenome = request.form.get('sobrenome')
        artista.data_nascimento = request.form.get('data_nascimento')

        try:
            db_session.commit()
            flash("Artista atualizada com sucesso!", "success")
            return redirect(url_for('artista_especifica', id_artista=id_artista))
        except Exception as e:
            db_session.rollback()
            flash("Erro ao atualizar artista.", "error")
            print(e)
        finally:
            db_session.close()

    db_session.close()
    return render_template('editar_artista.html', artista=artista)


@app.route('/musica/<int:id_musica>/editar_musica', methods=['GET', 'POST'])
def editar_musica(id_musica):
    db_session = local_session()
    musica = db_session.get(Musica, id_musica)

    if not musica:
        flash("Música não encontrada.", "error")
        return redirect(url_for('listar_musicas'))

    if request.method == 'POST':
        musica.nome = request.form.get('nome')
        musica.artista = request.form.get('artista')
        musica.album = request.form.get('album')
        musica.ano_lancamento = request.form.get('ano')

        try:
            db_session.commit()
            flash("Música atualizada com sucesso!", "success")
            return redirect(url_for('musica_especifica', id_musica=id_musica))
        except Exception as e:
            db_session.rollback()
            flash("Erro ao atualizar música.", "error")
            print(f'erro: {e}')
            db_session.close()
            return render_template('editar_musica.html', musica=musica)
        finally:
            db_session.close()

    db_session.close()
    return render_template('editar_musica.html', musica=musica)


@app.route('/albuns')
def listar_albuns():
    db_session = local_session()
    try:
        sql = select(Albuns)
        albuns = db_session.execute(sql).scalars().all()
        print("listar albuns", albuns)
        return render_template('listar_albuns.html', var_albuns=albuns)
    except SQLAlchemyError as e:
        print(f'Erro ao consultar albuns: {e}')
        flash('Erro ao carregar albuns', 'error')
        db_session.rollback()
        return redirect(url_for('pagina_inicial'))
    except Exception as e:
        db_session.rollback()
        flash('Erro inesperado', 'error')
        print(f'Erro ao consultar albuns##: {e}')
        return redirect(url_for('pagina_inicial'))
    finally:
        db_session.close()


# Adicionar nova música
@app.route('/adicionar_album', methods=['GET', 'POST'])
def adicionar_album():
    if request.method == 'POST':
        nome = request.form.get('nome')
        artista = request.form.get('artista')
        ano_lancamento = request.form.get('ano_lancamento')
        nome_musica = request.form.get('nome_musica')
        url_img = request.form.get('url_img')

        if not nome or not nome_musica:
            flash('Nome e nome da musica são obrigatórios!', 'error')
            return redirect(url_for('adicionar_album'))

        db_session = local_session()
        try:
            nova = Albuns(nome=nome, artista=artista, ano_lancamento=ano_lancamento, nome_musica=nome_musica,
                          url_img=url_img)
            db_session.add(nova)
            db_session.commit()
            flash('albunm adicionado com sucesso!', 'success')
            return redirect(url_for('listar_albuns'))
        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Erro ao salvar album!', 'error')
            print(e)
        finally:
            db_session.close()
    return render_template('adicionar_album.html')


# Ver detalhes de uma música
@app.route('/albuns/<int:id_albuns>')
def album_especifico(id_albuns):
    db_session = local_session()
    albuns = db_session.get(Albuns, id_albuns)
    db_session.close()
    if not albuns:
        flash('album não encontrado.', 'error')
        return redirect(url_for('listar_albuns'))
    return render_template('album_especifico.html', albuns=albuns)


@app.route('/albuns/<int:id_albuns>/deletar', methods=['POST', 'GET'])
def deletar_albuns(id_albuns):
    db_session = local_session()
    albuns = db_session.get(Albuns, id_albuns)
    if not albuns:
        flash('album não encontrado.', 'error')
        return redirect(url_for('listar_albuns'))
    try:
        db_session.delete(albuns)
        db_session.commit()
        flash('Album excluído com sucesso!', 'success')
    except Exception as e:
        db_session.rollback()
        flash('Erro ao excluir album.', 'error')
        print(e)
    finally:
        db_session.close()
    return redirect(url_for('listar_albuns'))


@app.route('/albuns/<int:id_albuns>/editar_albuns', methods=['GET', 'POST'])
def editar_albuns(id_albuns):
    db_session = local_session()
    albuns = db_session.get(Albuns, id_albuns)

    if not albuns:
        flash("Música não encontrada.", "error")
        return redirect(url_for('listar_albuns'))

    if request.method == 'POST':
        albuns.nome = request.form.get('nome')
        albuns.artista = request.form.get('artista')
        albuns.ano_lancamento = request.form.get('ano_lancamento')
        albuns.nome_musica = request.form.get('nome_musica')

        try:
            db_session.commit()
            flash("Album atualizado com sucesso!", "success")
            return redirect(url_for('album_especifica', id_albuns=id_albuns))
        except Exception as e:
            db_session.rollback()
            flash("Erro ao atualizar album.", "error")
            print(e)
        finally:
            db_session.close()

    db_session.close()
    return render_template('editar_albuns.html', albuns=albuns)


@app.route('/usuario', methods=['GET', 'POST'])
def usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not email or not senha:
            flash('Nome,email e senha são obrigatórios!', 'error')
            return redirect(url_for('usuario'))

        db_session = local_session()
        try:
            nova = Usuario(nome=nome, email=email, senha=senha)
            db_session.add(nova)
            db_session.commit()
            flash('Usuario cadastrado com sucesso!', 'success')
            return redirect(url_for('pagina_inicial'))
        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Erro ao salvar usuario!', 'error')
            print(e)
        finally:
            db_session.close()
    return render_template('usuario.html')


@app.route('/avaliacao/<id_musica>')
def avaliacao(id_musica):
    db_session = local_session()
    try:

        # Fazer um select para obter os ids dos usuários cadastrados
        sql= select(Usuario.id).where(Usuario.id != Avaliacao.id_usuario)
        ids_usuarios = db_session.execute(sql).scalars().all()
        print(ids_usuarios)

        # Com a lista dos ids escolher um aleatóriamente usando random
        id_usuario = random.choice(ids_usuarios)
        # -------------------------------------------------------------
        print("Usuário sorteado:", id_usuario)

        nova = Avaliacao(id_usuario=id_usuario, id_musica=int(id_musica))
        db_session.add(nova)
        db_session.commit()

        flash("Música curtida!", "success")
        return redirect(url_for('listar_musicas'))
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Erro ao curtir música!", "error")
        print(e)
        return redirect(url_for("listar_musicas"))


if __name__ == '__main__':
    app.run(debug=True)
