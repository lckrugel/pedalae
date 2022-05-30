from datetime import datetime, timedelta
import os
from . import create_app
from .models import Usuario, Item, Aluguel, Terminal
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
def get_usuario_documento(docUsuario):
    usuario = Usuario.query.filter_by(docUsuario=docUsuario).first()
    if usuario is None:
        abort(404)
    return jsonify(usuario.to_json()), 200


@app.route("/item/lista", methods=["GET"])
def get_itens():
    itens = Item.query.all()
    if itens is None:
        abort(404)
    return jsonify([item.to_json() for item in itens]), 200


@app.route("/terminal/lista", methods=["GET"])
def get_terminais():
    terminais = Terminal.query.all()
    if terminais is None:
        abort(404)
    return jsonify([terminal.to_json() for terminal in terminais]), 200


@app.route("/aluguel/lista", methods=["GET"])
def get_alugueis():
    alugueis = Aluguel.query.all()
    if alugueis is None:
        abort(404)
    return jsonify([aluguel.to_json() for aluguel in alugueis]), 200


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
        tipoItem=request.json.get('tipoItem'),
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


@app.route('/aluguel', methods=['POST'])
def post_aluguel():
    if not request.json:
        abort(400)
    aluguel = Aluguel(
        idItem=request.json.get('idItem'),
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
    usuario.nomeUsuario = request.json.get('nomeUsuario')
    usuario.docUsuario = request.json.get('docUsuario')
    usuario.saldoUsuario = request.json.get('saldoUsuario')
    db.session.commit()
    return jsonify(usuario.to_json()), 200


@app.route('/item/<int:idItem>', methods=['PUT'])
def put_item(idItem):
    if not request.json:
        abort(400)
    item = Item.query.get(idItem)
    if item is None:
        abort(404)
    item.tipoItem = request.json.get('tipoItem')
    item.descItem = request.json.get('descItem')
    item.terminalItem = request.json.get('terminalItem')
    item.proprietarioItem = request.json.get('proprietarioItem')
    db.session.commit()
    return jsonify(item.to_json()), 200


@app.route('/terminal/<int:idTerminal>', methods=['PUT'])
def put_terminal(idTerminal):
    if not request.json:
        abort(400)
    terminal = Item.query.get(idTerminal)
    if terminal is None:
        abort(404)
    terminal.nomeTerminal = request.json.get('nomeTerminal')
    terminal.localTerminal = request.json.get('localTerminal')
    db.session.commit()
    return jsonify(terminal.to_json()), 200


@app.route('/aluguel/<int:idAluguel>', methods=['PUT'])
def put_finaliza_aluguel(idAluguel):
    aluguel = Aluguel.query.get(idAluguel)
    if aluguel is None:
        abort(404)
    aluguel.fimAluguel = str(datetime.now())
    aluguel.tempoAluguel = str(datetime.now() - aluguel.inicioAluguel)
    aluguel.aluguelAtivo = False
    db.session.commit()
    return jsonify(aluguel.to_json()), 200


# -----------------------                DELETE             -----------------------------------------
@app.route('/usuario/<int:idUsuario>', methods=['DELETE'])
def delete_usuario(idUsuario):
    usuario = Usuario.query.get(idUsuario)
    if usuario is None:
        abort(404)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'result': True}), 200
