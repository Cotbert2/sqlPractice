#@authos: Mateo Garcia

#dependencies

from dotenv import load_dotenv
from flask import Flask, request
from flask_pymongo import PyMongo
from urllib.parse import quote_plus
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from constants import *
from validator import *
import os
from flask_cors import CORS



# Settings

app = Flask(__name__)

# Load environment variables

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWD = os.getenv('PASSWORD')

app.config['MONGO_URI'] = f"mongodb+srv://{USERNAME}:{PASSWD}@cluster0.4vufa.mongodb.net/espe?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true"

# Initialize PyMongo to work with MongoDB
mongoConnection = PyMongo(app)
CORS(app)

# Test DB connection

@app.route(test_db_connection, methods=['GET'])
def test_db_connection():
    try:
        mongoConnection.db.list_collection_names()
        return 'MongoDB connection: Success'
    except Exception as e:
        return f'MongoDB connection: Failed {e}'


# Routes
@app.route(all_users, methods=['GET'])
def get_all_users():
    try:
        users = mongoConnection.db.estudiantes.find()
        response = []
        for user in users:
            user['_id'] = str(user['_id'])
            response.append(user)
        return {
            'data': response,
            'status': 200
        }
    except :
        return internal_server_error()


@app.route(user_by_id, methods=['GET'])
def get_user_by_id(id):
    print('buscar usuario por id', id)
    try:
        user = mongoConnection.db.estudiantes.find_one({'username': id})
        if user:
            user['_id'] = str(user['_id'])
            return {
                'data': user,
                'status': 200
            }
        else:
            return not_found()
    except:
        return internal_server_error()



@app.route(all_users, methods=['POST'])
def create_user():
    print('crear usuario')
    try:
        username = request.json['username']
        nombre = request.json['nombre']
        apellido = request.json['apellido']
        correo = request.json['correo']
        fecha_nacimiento = request.json['fechaDeNacimiento']
        direccion = request.json['direccion']
        edad = request.json['edad']
        genero = request.json['genero']
        password = request.json['password']
        trabajo = request.json['trabajo']
        materias_que_toma = request.json['materiasQueToma']

        #check for all fields into request to create a user
        if not username or not nombre or not apellido or not correo or not fecha_nacimiento or not direccion or not edad or not genero or not password or not trabajo or not materias_que_toma:
            return bad_request()



        if not validate_email(correo):
            return bad_request()
    except:
        return bad_request()

    # if username and email and password:
    password = generate_password_hash(password)
    mongoConnection.db.estudiantes.insert_one(
        {
            'username': username,
            'nombre': nombre,
            'apellido': apellido,
            'correo': correo,
            'fechaDeNacimiento': fecha_nacimiento,
            'direccion': direccion,
            'edad': edad,
            'genero': genero,
            'password': password,
            'trabajo': trabajo,
            'materiasQueToma': materias_que_toma
        }
    )
    print('Usuario creado' + username)
    # else:
    #     return bad_request()
    return {
        'message': 'User creado con exito',
        'status': 201
    }


@app.route(user_by_id, methods=['PUT'])
def update_user(id):
    try:
        username = request.json['username']
        nombre = request.json['nombre']
        apellido = request.json['apellido']
        correo = request.json['correo']
        fecha_nacimiento = request.json['fechaDeNacimiento']
        direccion = request.json['direccion']
        edad = request.json['edad']
        genero = request.json['genero']
        password = request.json['password']


    except:
        return bad_request()

    if username and nombre and apellido and correo and fecha_nacimiento and direccion and edad and genero and password:
        password = generate_password_hash(password)
        result = mongoConnection.db.estudiantes.update_one(
            {'username': id},
            {
                '$set': {
                    'username': username,
                    'nombre': nombre,
                    'apellido': apellido,
                    'correo': correo,
                    'fechaDeNacimiento': fecha_nacimiento,
                    'direccion': direccion,
                    'edad': edad,
                    'genero': genero,
                    'password': password
                }
            }
        )
        if result.modified_count > 0:
            return {
                'message': 'Usuario actualizado con exito',
                'status': 200
            }
        else:
            return not_found()
    else:
        return bad_request()

@app.route(user_by_id, methods=['DELETE'])
def delete_user(id):
    try:
        result = mongoConnection.db.estudiantes.delete_one({'username': id})
        if result.deleted_count > 0:
            return {
                'message': 'Usuario eliminado con exito',
                'status': 200
            }
        else:
            return not_found()
    except:
        return internal_server_error()




# Error Handlers

@app.errorhandler(400)
def bad_request(error = None):
    message = {
        'message': 'Petición incorrecta: ',
        'status': 400
    }
    return message


@app.errorhandler(404)
def not_found(error = None):
    message = {
        'message': 'Recurso no encontrado: ',
        'status': 404
    }
    return message


@app.errorhandler(500)
def internal_server_error(error = None):
    message = {
        'message': 'Error interno del servidor: ',
        'status': 500
    }
    return message




if __name__ == '__main__':
    print(f"Credentials: {USERNAME} {PASSWD}")
    app.run(port=8000, debug=True)
