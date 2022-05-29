from . import db


class Usuario(db.Model):
    __tablename__ = 'usuario'
    idUsuario = db.Column(db.Integer, primary_key=True)
    nomeUsuario = db.Column(db.String(50), nullable=False)
    docUsuario = db.Column(db.String(15), nullable=False)
    saldoUsuario = db.Column(db.Numeric(19, 4), nullable=False)
    itens = db.relationship('Item', backref=db.backref('proprietario', lazy=True))
    alugueis = db.relationship('Aluguel', backref=db.backref('locatario', lazy=True))

    def to_json(self):
        return {
            'idUsuario': self.idUsuario,
            'nomeUsuario': self.nomeUsuario,
            'docUsuario': self.docUsuario,
            'saldoUsuario': self.saldoUsuario
        }


class Item(db.Model):
    __tablename__ = 'item'
    idItem = db.Column(db.Integer, primary_key=True)
    tipoItem = db.Column(db.String(50), nullable=False)
    descItem = db.Column(db.String(100), nullable=True)
    terminalItem = db.Column(db.Integer, db.ForeignKey('terminal.idTerminal'), nullable=False)
    proprietarioItem = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    alugueis = db.relationship('Aluguel', backref=db.backref('item', lazy=True))

    def to_json(self):
        return {
            'idItem': self.idItem,
            'terminalItem': self.terminalItem,
            'proprietarioItem': self.proprietarioItem
        }


class Terminal(db.Model):
    __tablename__ = 'terminal'
    idTerminal = db.Column(db.Integer, primary_key=True)
    nomeTerminal = db.Column(db.String(50), nullable=False)
    localTerminal = db.Column(db.String(100), nullable=False)
    itens = db.relationship('Item', backref=db.backref('terminal', lazy=True))

    def to_json(self):
        return {
            'idTerminal': self.idTerminal,
            'nomeTerminal': self.nomeTerminal,
            'localTerminal': self.localTerminal
        }


class Aluguel(db.Model):
    __tablename__ = 'aluguel'
    idAluguel = db.Column(db.Integer, primary_key=True)
    idItem = db.Column(db.Integer, db.ForeignKey('item.idItem'), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    inicioAluguel = db.Column(db.DateTime, nullable=False)
    fimAluguel = db.Column(db.DateTime, nullable=True)
    tempoAluguel = db.Column(db.Time, nullable=True)
    aluguelAtivo = db.Column(db.Boolean, nullable=False)

    def to_json(self):
        return {
            'idAluguel': self.idAluguel,
            'idItem': self.idItem,
            'idUsuario': self.idUsuario,
            'inicioAluguel': self.inicioAluguel,
            'fimAluguel': self.fimAluguel,
            'tempoAluguel': self.fimAluguel,
            'aluguelAtivo': self.aluguelAtivo
        }
