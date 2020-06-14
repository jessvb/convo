import json
from app import logger, db
from datetime import datetime
from helpers import convert_to_object, convert_to_dict

class User(db.Model):
    '''User model that is associated with Convo clients'''
    id = db.Column(db.Integer, primary_key=True)
    # Server ID of connected client
    sid = db.Column(db.String(120), unique=True, nullable=False)
    # Date when created
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Date when user last connected
    connected_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Program(db.Model):
    '''Program model that is currently representing procedures in Convo'''
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(120), db.ForeignKey('user.sid'), nullable=False)
    # Name of procedure
    name = db.Column(db.String(80), nullable=False)
    # JSON-encoded string of the procedure object
    procedure = db.Column(db.Text, nullable=True)
    # Date when created
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Date when updated
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def get_or_create_user(client):
    '''Gets user based on client if exists, else creates a new user'''
    user = User.query.filter_by(sid=client.id).first()

    if user is None:
        user = User(sid=client.id)
        db.session.add(user)
    else:
        user.connected_on = datetime.utcnow()

    db.session.commit()
    return user

def from_db_program(program):
    '''Convert Program DB model to a Procedure'''
    return json.loads(program.procedure, object_hook=convert_to_object)

def get_procedures(sid):
    '''Get all procedures of a client based on their sid'''
    programs = Program.query.filter_by(sid=sid).all()
    if not programs:
        return {}

    procedures = [(program.name, from_db_program(program)) for program in programs]
    return dict(procedures)

def add_or_update_procedure(sid, procedure):
    '''Add or update an existing procedure based on client's sid and procedure's id'''
    encoded = json.dumps(procedure, default=convert_to_dict)

    program = Program.query.filter_by(sid=sid, name=procedure.name).first()
    if program is None:
        program = Program(sid=sid, name=procedure.name, procedure=encoded)
        db.session.add(program)
    else:
        program.procedure = encoded
        program.updated_on = datetime.utcnow()

    db.session.commit()
    procedure.id = program.id

    return program

def remove_procedure(sid, procedure):
    '''Removes a procedure from database'''
    program = Program.query.filter_by(sid=sid, name=procedure.name).first()
    if not program:
        return

    db.session.delete(program)
    db.session.commit()
