from flask import jsonify,session, Blueprint, current_app, request
from werkzeug.security import check_password_hash, generate_password_hash
from sportsbetx.db import get_db
from sportsbetx.from_protos import user_service_pb2, user_service_pb2_grpc
import jwt, datetime, functools, grpc

bp = Blueprint('auth',__name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        email,password = data['email'],data['password']
        token, is_valid = validate_login(data)
        if is_valid:
            session.clear() # clear previous user once logged in
            session['user_id'] = email
            return jsonify({"message": "Login successful", "token": token}), 200
        else:
            session.clear()
            return jsonify({"message": f"Login error: {token}"}), 403
    except(Exception) as err:
        return jsonify({"status":"Server Error", "message":f"Error with: {repr(err)}"}), 500

@bp.route('/logout')
def logout():
    # blacklist_token()
    session.clear()    
    return jsonify({"message":"Logout successful"}), 200

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        val_error = validate_register(username=data['username'],email=data['email'],
                                    password=data['password'],role=data['role'])
        if val_error is None:
            with grpc.insecure_channel('localhost:40051') as channel:
                stub = user_service_pb2_grpc.UserMgtStub(channel)
                response = user_service_create(stub,data) # communicate with user mgt microservice

            if(response[0]==True):        
                return jsonify({"message": "User created. Please login"}), 200
            else:
                return jsonify({"message": f"MongoProvider {response[1]}"}), 500
        else:
            return jsonify({"message": f"{val_error}"}), 403

    except(Exception) as err:
        print(f"Error with: {err}")
        return jsonify({"status":"Server Error", "message":f"Error with: {err}"}), 500

def admin_only(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        role = session.get('role')
        if role == 'admin':
            session['role'] = None # maintain essence of decoding auth_token for each protected request
            return view(**kwargs)
        else:
            session['role'] = None
            return jsonify({"message": f"Action is restricted from {role} priviledge"}), 403
    return wrapped_view

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):   
        try:     
            auth_token = request.headers.get('Authorization')
            if auth_token:
                auth_token = auth_token.split(' ')[1]     
                result, role, is_token = decode_auth_token(auth_token)
                if is_token and (result == session.get('user_id')): # also becomes false when session is no longer valid.
                    session['role'] = role
                    return view(**kwargs)
                else:
                    return jsonify({"status":"auth error","message": result}), 403
            else:
                return jsonify({"message": "Authorization required"}), 403
        except(Exception) as err:
            return jsonify({"status":"Server Error", "message":f"Error with: {repr(err)}"}), 500
                     
    return wrapped_view


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'),algorithms=['HS256'])
        return (payload['sub'], payload['role'], True)
    except jwt.ExpiredSignatureError:
        return ('Signature expired. Please log in again.',None, False)
    except jwt.InvalidTokenError:
        return ('Invalid token. Please log in again.',None, False)

def validate_login(data):
    with grpc.insecure_channel('localhost:40051') as channel:
        stub = user_service_pb2_grpc.UserMgtStub(channel)
        response = user_service_read(stub,data) # communicate with user mgt microservice

    return(response[1],response[0])

def validate_register(**kwargs):
    # improve with regex 
    for key,value in kwargs.items():
        if value == "":
            return f"{key} field can't be empty"
    
    return None

def user_service_create(stub,data):
    sent_data = user_service_pb2.UserDataDict(**data)
    returned = stub.CreateUser(sent_data)
    return (returned.status,returned.message)

def user_service_read(stub,data):
    sent_data = user_service_pb2.UserDataDict(**data)
    returned = stub.ReadUser(sent_data)
    return (returned.status,returned.message,returned.data)