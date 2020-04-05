import json
from app import logger, db
from helpers import convert_to_object, convert_to_dict

class User(db.Model):
    '''User model that is associated with Convo clients'''
    id = db.Column(db.Integer, primary_key=True)
    # Server ID of connected client
    sid = db.Column(db.String(120), unique=True, nullable=False)

class Program(db.Model):
    '''Program model that is currently representing procedures in Convo'''
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(120), db.ForeignKey('user.sid'), nullable=False)

    # Name of procedure
    name = db.Column(db.String(80), nullable=False)

    # JSON-encoded string of the procedure object
    encoded = db.Column(db.Text, nullable=True)

def get_user(sid):
    '''Gets user by sid'''
    return User.query.filter_by(sid=sid).first()

def add_user(client):
    '''Add user to database'''
    user = User(sid=client.id)
    db.session.add(user)
    db.session.commit()
    return user.id

def from_db_program(program):
    '''Convert Program DB model to a Procedure'''
    return json.loads(program.encoded, object_hook=convert_to_object)

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

    # Procedure exists in database only if property id is set
    # This can be used to check for existence of procedure in database
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
    '''Removes a procedure from database'''
    program = Program.query.filter_by(id=procedure.id).first()
    if not program:
        return

    db.session.delete(program)
    db.session.commit()
