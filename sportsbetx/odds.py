from flask import Blueprint, request, jsonify, session
from sportsbetx.from_protos import odds_crud_pb2_grpc, odds_crud_pb2
from sportsbetx.auth import login_required, admin_only
import grpc

bp = Blueprint('odds', __name__, url_prefix='/odds') 

@bp.route('/create', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    try:  
        val_error = validate_create(league=data['league'], home_team=data['home_team'], away_team=data['away_team'], 
                    home_team_win_odds=data['home_team_win_odds'], away_team_win_odds=data['away_team_win_odds'],
                    draw_odds=data['draw_odds'],game_date=data['game_date'] )

        if val_error is None:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = odds_crud_pb2_grpc.OddsCrudStub(channel)
                response = odds_service_create(stub,data)   # communicate with odds_crud microservice
              
            print(response[0])
            if(response[0]==True):        
                return jsonify({"message": "Odds created"}), 200
            else:
                return jsonify({"message": f"Odds CRUD Service: {response[1]}"}), 500
              
        else:
            return jsonify({"message": f"{val_error}"}), 403    

    except(Exception,KeyError) as err:
            print(f"Error with: {err}")
            return jsonify({"status":"Server Error", "message":f"Error with: {err}"}), 500

@bp.route('/read')
@login_required
def read():
    data = request.get_json()
    try:
        league, date_range = data['league'], data['date_range']
        val_error = validate_create(league=league,date_range=date_range)    

        if val_error is None:            
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = odds_crud_pb2_grpc.OddsCrudStub(channel)
                response = odds_service_read(stub,data)  

            if(response[0]==True):
                sorte = filter_by_current_user(response[2])        
                return jsonify({"message": "Odds read", "data": sorte}), 200
            else:
                return jsonify({"message": f"Odds CRUD Service: {response[1]}"}), 500
              
        else:
            return jsonify({"message": f"{val_error}"}), 403

    except(Exception,KeyError) as err:
            print(f"Error with: {err}")
            return jsonify({"status":"Server Error", "message":f"Error with: {err}"}), 500 

@bp.route('/update', methods=['POST'])
@login_required
@admin_only
def update():
    data = request.get_json()
    try: 
        val_error = validate_create(league=data['league'], home_team=data['home_team'], away_team=data['away_team'], 
                    home_team_win_odds = data['home_team_win_odds'], away_team_win_odds= data['away_team_win_odds'],
                    draw_odds=data['draw_odds'],game_date=data['game_date'], odds_id = data['odds_id'])
        if val_error is None:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = odds_crud_pb2_grpc.OddsCrudStub(channel)
                response = odds_service_update(stub,data)   # communicate with odds_crud microservice

            if(response[0]==True):        
                return jsonify({"message": "Odds updated"}), 200
            else:
                return jsonify({"message": f"Odds CRUD Service {response[1]}"}), 500
              
        else:
            return jsonify({"message": f"{val_error}"}), 403    

    except(Exception,KeyError) as err:
            print(f"Error with: {err}")
            return jsonify({"status":"Server Error", "message":f"Error with: {err}"}), 500

@bp.route('/delete', methods=['POST'])
@login_required
@admin_only
def delete():
    data = request.get_json()
    try:      
        val_error = validate_create(league=data['league'], home_team=data['home_team'], 
            away_team=data['away_team'],game_date=data['game_date'])

        if val_error is None:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = odds_crud_pb2_grpc.OddsCrudStub(channel)
                response = odds_service_delete(stub,data)   # communicate with odds_crud microservice
            
            if(response[0]==True):        
                return jsonify({"message": "Odds deleted"}), 200
            else:
                return jsonify({"message": f"Odds CRUD service {response[1]}"}), 500
              
        else:
            return jsonify({"message": f"{val_error}"}), 403    

    except(Exception,KeyError) as err:
            print(f"Error with: {err}")
            return jsonify({"status":"Server Error", "message":f"Error with: {repr(err)}"}), 500

   
def validate_create(**kwargs):
    # improve with reqex 
    for key,value in kwargs.items():
        if value == "":
            return f"{key} field can't be empty"
    return None

def filter_by_current_user(data: 'dict'):
    """User should see only their odds, admins can see all"""
    role, email = session.get('role'), session.get('user_id')
    new_data = []
    if role == 'admin':
        return data['list']
    for row in data['list']:
        if email in row:
            new_data.append(odds_to_dict(row))
    return new_data
        
def odds_to_dict(data_row):
    return {
        "id": data_row[0],
        "league": data_row[1],
        "home_team": data_row[2],
        "away_team": data_row[3],
        "home_team_win_odds": data_row[4],
        "away_team_win_odds":data_row[5],
        "draw_odds":data_row[6],
        "game_date":data_row[7]
    }

def odds_service_create(stub,data):
    sent_data = odds_crud_pb2.DataDict(**data,user_id=session.get('user_id'))
    returned = stub.CreateOdds(sent_data)
    return (returned.status,returned.message)

def odds_service_read(stub,data):
    sent_data = odds_crud_pb2.DataDict(**data)
    received = {"list":[]}
    for returned in stub.ReadOdds(sent_data):
        received["list"].append(fromDataDict(returned.data))
    return (returned.status,returned.message, received)

def fromDataDict(data: odds_crud_pb2.DataDict):
    return {
        "odds_id": data.odds_id,
        "league": data.league,
        "home_team": data.home_team,
        "away_team": data.away_team,
        "home_team_win_odds": data.home_team_win_odds,
        "away_team_win_odds":data.away_team_win_odds,
        "draw_odds":data.draw_odds,
        "game_date":data.game_date
    }

def odds_service_update(stub,data):
    sent_data = odds_crud_pb2.DataDict(**data)
    returned = stub.UpdateOdds(sent_data)
    return (returned.status,returned.message)

def odds_service_delete(stub,data):
    sent_data = odds_crud_pb2.DataDict(**data)
    returned = stub.DeleteOdds(sent_data)
    return (returned.status,returned.message)