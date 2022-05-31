from datetime import datetime, timedelta
import os
from . import create_app
from .models import Usuario, Item, Aluguel, Terminal, HistoricoAluguel
from . import db
from flask import jsonify, request, abort

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# -----------------------                GET              -----------------------------------------
@app.route("/usuario/lista", methods=["GET"])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_json() for usuario in usuarios]), 200


@app.route("/usuario/<int:idUsuario>", methods=["GET"])
def get_usuario(idUsuario):
    usuario = Usuario.query.get(idUsuario)
    if usuario is None:
        abort(404)
    return jsonify(usuario.to_json()), 200


@app.route("/usuario/documento/<string:docUsuario>", methods=["GET"])
def get_usuario_doc(docUsuario):
    usuario = Usuario.query.filter_by(docUsuario=docUsuario).first()
    if usuario is None:
        abort(404)
    return jsonify(usuario.to_json()), 200


@app.route("/usuario/<int:idUsuario>/itens", methods=["GET"])
def get_usuario_itens(idUsuario):
    usuario = Usuario.query.get(idUsuario)
    if usuario is None:
        abort(404)
    return jsonify([item.to_json() for item in usuario.itens]), 200


@app.route("/usuario/<int:idUsuario>/alugueis", methods=["GET"])
def get_usuario_alugueis(idUsuario):
    usuario = Usuario.query.get(idUsuario)
    if usuario is None:
        abort(404)
    return jsonify([aluguel.to_json() for aluguel in usuario.alugueis]), 200


@app.route("/usuario/<int:idUsuario>/hist_alugueis", methods=["GET"])
def get_usuario_hist_alugueis(idUsuario):
    usuario = Usuario.query.get(idUsuario)
    if usuario is None:
        abort(404)
    return jsonify([hist_aluguel.to_json() for hist_aluguel in usuario.historicoAlugueis]), 200


@app.route("/item/lista", methods=["GET"])
def get_itens():
    itens = Item.query.all()
    if itens is None:
        abort(404)
    return jsonify([item.to_json() for item in itens]), 200


@app.route("/item/<int:idItem>", methods=["GET"])
def get_item(idItem):
    item = Item.query.get(idItem)
    if item is None:
        abort(404)
    return jsonify(item.to_json()), 200


@app.route("/item/<int:idItem>/hist_alugueis", methods=["GET"])
def get_item_hist_alugueis(idItem):
    item = Usuario.query.get(idItem)
    if item is None:
        abort(404)
    return jsonify([hist_aluguel.to_json() for hist_aluguel in item.historicoAlugueis]), 200


@app.route("/terminal/lista", methods=["GET"])
def get_terminais():
    terminais = Terminal.query.all()
    if terminais is None:
        abort(404)
    return jsonify([terminal.to_json() for terminal in terminais]), 200


@app.route("/terminal/<int:idTerminal>/itens", methods=["GET"])
def get_terminal_itens(idTerminal):
    terminal = Terminal.query.get(idTerminal)
    if terminal is None:
        abort(404)
    return jsonify([item.to_json() for item in terminal.itens]), 200


@app.route("/terminal/<int:idTerminal>", methods=["GET"])
def get_terminal(idTerminal):
    terminal = Terminal.query.get(idTerminal)
    if terminal is None:
        abort(404)
    return jsonify(terminal.to_json()), 200


@app.route("/aluguel/lista", methods=["GET"])
def get_alugueis():
    alugueis = Aluguel.query.all()
    if alugueis is None:
        abort(404)
    return jsonify([aluguel.to_json() for aluguel in alugueis]), 200


@app.route("/aluguel/<int:idAluguel>", methods=["GET"])
def get_aluguel(idAluguel):
    aluguel = Aluguel.query.get(idAluguel)
    if aluguel is None:
        abort(404)
    return jsonify(aluguel.to_json()), 200


@app.route("/hist_aluguel/lista", methods=["GET"])
def get_hist_alugueis():
    hist_alugueis = HistoricoAluguel.query.all()
    if hist_alugueis is None:
        abort(404)
    return jsonify([hist_aluguel.to_json() for hist_aluguel in hist_alugueis]), 200


@app.route("/hist_aluguel/<int:idHistorico>", methods=["GET"])
def get_hist_aluguel(idHistorico):
    hist_aluguel = HistoricoAluguel.query.get(idHistorico)
    if hist_aluguel is None:
        abort(404)
    return jsonify(hist_aluguel.to_json()), 200


# -----------------------                POST - CREATE             -----------------------------------
@app.route('/usuario', methods=['POST'])
def post_usuario():
    if not request.json:
        abort(400)
    usuario = Usuario(
        nomeUsuario=request.json.get('nomeUsuario'),
        docUsuario=request.json.get('docUsuario'),
        saldoUsuario=request.json.get('saldoUsuario')
    )
    db.session.add(usuario)
    db.session.commit()
    return jsonify(usuario.to_json()), 201


@app.route('/item', methods=['POST'])
def post_item():
    if not request.json:
        abort(400)
    item = Item(
        descItem=request.json.get('descItem'),
        terminalItem=request.json.get('terminalItem'),
        proprietarioItem=request.json.get('proprietarioItem')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json()), 201


@app.route('/terminal', methods=['POST'])
def post_terminal():
    if not request.json:
        abort(400)
    terminal = Terminal(
        nomeTerminal=request.json.get('nomeTerminal'),
        localTerminal=request.json.get('localTerminal')
    )
    db.session.add(terminal)
    db.session.commit()
    return jsonify(terminal.to_json()), 201


# Não permite criar um aluguel com um item que já esteja em um aluguel
@app.route('/aluguel', methods=['POST'])
def post_aluguel():
    if not request.json:
        abort(400)
    iditem = request.json.get('idItem')
    if Aluguel.query.get(iditem) is not None:
        abort(406)
    aluguel = Aluguel(
        idItem=iditem,
        idUsuario=request.json.get('idUsuario'),
        inicioAluguel=datetime.now()
    )
    db.session.add(aluguel)
    db.session.commit()
    return jsonify(aluguel.to_json()), 201


# -----------------------                PUT - UPDATE             -----------------------------------
@app.route('/usuario/<int:idUsuario>', methods=['PUT'])
def put_usuario(idUsuario):
    if not request.json:
        abort(400)
    usuario = Usuario.query.get(idUsuario)
    if usuario is None:
        abort(404)
    usuario.nomeUsuario = request.json.get('nomeUsuario') or usuario.nomeUsuario
    usuario.docUsuario = request.json.get('docUsuario') or usuario.docUsuario
    usuario.saldoUsuario = request.json.get('saldoUsuario') or usuario.saldoUsuario
    db.session.commit()
    return jsonify(usuario.to_json()), 200


@app.route('/item/<int:idItem>', methods=['PUT'])
def put_item(idItem):
    if not request.json:
        abort(400)
    item = Item.query.get(idItem)
    if item is None:
        abort(404)
    item.descItem = request.json.get('descItem') or item.descItem
    item.terminalItem = request.json.get('terminalItem') or item.terminalItem
    item.proprietarioItem = request.json.get('proprietarioItem') or item.proprietarioItem
    db.session.commit()
    return jsonify(item.to_json()), 200


@app.route('/terminal/<int:idTerminal>', methods=['PUT'])
def put_terminal(idTerminal):
    if not request.json:
        abort(400)
    terminal = Terminal.query.get(idTerminal)
    if terminal is None:
        abort(404)
    terminal.nomeTerminal = request.json.get('nomeTerminal') or terminal.nomeTerminal
    terminal.localTerminal = request.json.get('localTerminal') or terminal.localTerminal
    db.session.commit()
    return jsonify(terminal.to_json()), 200


# -----------------------                DELETE             -----------------------------------------
# Deleta usuario e todos os itens do qual ele é proprietario. Não deleta se tiver aluguel ativo
@app.route('/usuario/<int:idUsuario>', methods=['DELETE'])
def delete_usuario(idUsuario):
    usuario = Usuario.query.get(idUsuario)
    if usuario is None:
        abort(404)
    if Aluguel.query.filter_by(idUsuario=idUsuario).first() is not None:
        abort(405)
    for item in usuario.itens:
        db.session.delete(item)
        db.session.commit()
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'result': True}), 200


# Deleta item e o historico de alugueis referentes ao item. Não deleta se tiver aluguel ativo
@app.route('/item/<int:idItem>', methods=['DELETE'])
def delete_item(idItem):
    item = Item.query.get(idItem)
    if item is None:
        abort(404)
    if item.aluguel is not None:
        abort(405)
    for hist_aluguel in item.historicoAlugueis:
        db.session.delete(hist_aluguel)
        db.session.commit()
    db.session.delete(item)
    db.session.commit()
    return jsonify({'result': True}), 200


# Não deleta o terminal se tiver itens associados a ele
@app.route('/terminal/<int:idTerminal>', methods=['DELETE'])
def delete_terminal(idTerminal):
    terminal = Terminal.query.get(idTerminal)
    if terminal is None:
        abort(404)
    if Item.query.filter_by(terminalItem=idTerminal).first() is not None:
        abort(405)
    db.session.delete(terminal)
    db.session.commit()
    return jsonify({'result': True}), 200


# Deleta aluguel sem adicioná-lo ao histórico.
@app.route('/aluguel/<int:idAluguel>', methods=['DELETE'])
def delete_aluguel(idAluguel):
    aluguel = Aluguel.query.get(idAluguel)
    if aluguel is None:
        abort(404)
    db.session.delete(aluguel)
    db.session.commit()
    return jsonify({'result': True}), 200


@app.route('/hist_aluguel/<int:idHistorico>', methods=['DELETE'])
def delete_hist_aluguel(idHistorico):
    hist_aluguel = HistoricoAluguel.query.get(idHistorico)
    if hist_aluguel is None:
        abort(404)
    db.session.delete(hist_aluguel)
    db.session.commit()
    return jsonify({'result': True}), 200


# Finaliza (deleta) um aluguel mas antes cria uma entrada em HistoricoAluguel com os dados do aluguel
@app.route('/aluguel/finaliza/<int:idAluguel>', methods=['DELETE'])
def finaliza_aluguel(idAluguel):
    aluguel = Aluguel.query.get(idAluguel)
    if Aluguel is None:
        abort(404)
    hist_aluguel = HistoricoAluguel(
        idAluguel=aluguel.idAluguel,
        idItem=aluguel.idItem,
        idUsuario=aluguel.idUsuario,
        docUsuario=aluguel.locatario.docUsuario,
        inicioAluguel=aluguel.inicioAluguel,
        fimAluguel=datetime.now(),
        tempoAluguel=datetime.now() - aluguel.inicioAluguel
    )
    db.session.add(hist_aluguel)
    db.session.delete(aluguel)
    db.session.commit()
    return jsonify({'result': True}, hist_aluguel.to_json()), 200

