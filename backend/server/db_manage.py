import json
from app import logger, db
from helpers import convert_to_object, convert_to_dict

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(120), unique=True, nullable=False)

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(120), db.ForeignKey('user.sid'), nullable=False)
    encoded = db.Column(db.Text, nullable=True)

def get_user(sid):
    return User.query.filter_by(sid=sid).first()

def add_user(client):
    user = User(client.id)
    db.session.add(user)
    db.session.commit()
    return user.id

def from_db_program(proc):
    return json.loads(proc.encoded, object_hook=convert_to_object)

def get_programs(sid):
    programs = Procedure.query.filter_by(sid=sid).all()
    return [from_db_program(program) for program in programs]

def add_program(sid, proc):
    encoded = json.dumps(proc, default=convert_to_dict)
    program = Program(sid, encoded)
    db.session.add(program)
    db.session.commit()
    return program.id

def update_program(pid, proc):
    program = Procedure.query.filter_by(id=pid).first()
    program.encoded = json.dumps(proc, default=convert_to_dict)
    db.session.commit()
    return program.id
