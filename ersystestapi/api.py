import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

api_bg = Blueprint('api', __name__, url_prefix='/api')

@api_bg.route('/clients', methods=('GET',))
def list_client():
    db = get_db()
    results = db.execute('''
        SELECT 
            c.id, 
            c.name, 
            c.email, 
            c.phone,
            p.id as provider_id, 
            p.name as provider_name
        FROM clients as c
        JOIN clients_providers as cp ON cp.client_id=c.id
        JOIN providers as p  ON p.id=cp.provider_id
    ''')

    def check_client(email, clients):
        for item in clients:
            if email == item['email']:
                return item
        return False

    response = []
    for item in results.fetchall():
        if find_client:= check_client(item['email'], response):
            find_client['providers'].append({"id": item['provider_id'], "name": item['provider_name']})
        else:
            client = {}
            client['name'] = item['name']
            client['email'] = item['email']
            client['phone'] = item['phone']
            client['providers'] = [{"id": item['provider_id'], "name": item['provider_name']}]

            response.append(client)

    # print(response)
    # response = [
    #     {
    #         "id": item['id'], 
    #         "name": item['name'], 
    #         "email": item['email'], 
    #         "phone": item['phone'], 
    #         "providers": item['providers']
    #     } 
    #     for item 
    #     in results.fetchall()]
    return jsonify({"count": len(response), "status": 200, "data": response}), 200


@api_bg.route('/create-client-with-providers', methods=('POST',))
def create_client_with_providers():
    db = get_db()
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    providers = data['providers']

    if not name or not email or not phone or not providers:
        return jsonify({"message": "All fields are required", "status": 400}), 400

    try:
        db.execute("INSERT INTO clients(name, email, phone) VALUES(?, ?, ?)", (name, email, phone))
        db.commit()
        client = db.execute('SELECT id FROM clients WHERE email=?', (email,)).fetchone()
        client_providers_data = [(client['id'], p) for p in providers]
        print(client_providers_data)
        db.executemany("INSERT INTO clients_providers VALUES(?, ?)", client_providers_data)
        db.commit()
    except db.IntegrityError:
        return jsonify({"message": "Email already exist"}), 400
    except db.Error as e:
        return jsonify({"message": e.message}), 400

    return jsonify({"message": "Client successfully saved", "status": 201}), 201


@api_bg.route('/providers', methods=('GET', 'POST'))
def list_or_create_provider():
    db = get_db()

    if request.method == 'GET':
        results = db.execute("SELECT * FROM providers")
        response = [{"id": item['id'], "name": item['name']} for item in results.fetchall()]
        return jsonify({"count": len(response), "status": 200, "data": response}), 200

    if request.method == 'POST':
        data = request.get_json()
        name = data['name']

        if not name:
            return jsonify({"message": "Name is required", "status": 400}), 400

        try:
            db.execute("INSERT INTO providers(name) VALUES(?)", (name,))
            db.commit()
        except db.Error as e:
            return jsonify({"message": e.message}), 400

        return jsonify({"message": "Provider successfully saved", "status": 201}), 201