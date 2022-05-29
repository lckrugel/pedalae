import os
from . import create_app
from .models import Usuario
from . import db
from flask import jsonify, request, abort

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.route("/usuario/lista", methods=["GET"])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_json() for usuario in usuarios])


@app.route("/usuario/<int:idUsuario>", methods=["GET"])
def get_usuario(idUsuario):
    usuario = Usuario.query.get(idUsuario)
    if usuario is None:
        abort(404)
    return jsonify(usuario.to_json())


@app.route("/usuario/documento/<string:docUsuario>", methods=["GET"])
def get_usuario_documento(docUsuario):
    usuario = Usuario.query.filter_by(docUsuario=docUsuario).first()
    if usuario is None:
        abort(404)
    return jsonify(usuario.to_json())



