import json
from app import logger, db
from helpers import convert_to_object, convert_to_dict

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(120), unique=True, nullable=False)

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(120), db.ForeignKey('user.sid'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    encoded = db.Column(db.Text, nullable=True)

def get_user(sid):
    return User.query.filter_by(sid=sid).first()

def add_user(client):
    user = User(sid=client.id)
    db.session.add(user)
    db.session.commit()
    return user.id

def from_db_program(proc):
    return json.loads(proc.encoded, object_hook=convert_to_object)

def get_procedures(sid):
    programs = Program.query.filter_by(sid=sid).all()
    if not programs:
        return {}

    procedures = [(program.name, from_db_program(program)) for program in programs]
    return dict(procedures)

def add_or_update_procedure(sid, procedure):
    encoded = json.dumps(procedure, default=convert_to_dict)

    if procedure.id is None:
        program = Program(sid=sid, name=procedure.name, encoded=encoded)
        db.session.add(program)
    else:
        program = Program.query.filter_by(id=procedure.id).first()
        program.encoded = encoded

    db.session.commit()
    procedure.id = program.id
    return program.id

def remove_procedure(procedure):
    program = Program.query.filter_by(id=procedure.id).first()
    if not program:
        return

    db.session.delete(program)
    db.session.commit()
