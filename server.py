# Name:
# Date:
# Assignment: hw4
# File: server.py
# Description: Simple Python Flask Web Server to build a REST API.

from flask import Flask, request, jsonify

app = Flask(__name__)

PORT = 8080
HOST = "127.0.0.1"

test_data = [
    {"id": 1, "name": "test1", "address": "123", "email": "test1@test.com"},
    {"id": 2, "name": "test2", "address": "123", "email": "test2@test.com"},
    {"id": 3, "name": "test3", "address": "123", "email": "test3@test.com"},
]

user_data = [
	{"id": 1, "name": "Kane", "type": "admin"},
	{"id": 2, "name": "John", "type": "reader"},
	{"id": 3, "name": "Jim", "type": "author"}
]

recipe_data = [
	{"id": 1, "user_id": 1, "steps": "bake cookies"},
	{"id": 2, "user_id": 1, "steps": "(1) clean rice (2) cook rice (3) eat rice"}
]
	


def _find_next_id(data_list: list):
    """Small helper function to find the next ID from a previous list of data"""
    return max(data["id"] for data in data_list) + 1


@app.get("/api/v1/test")
def get_test_data():
    return jsonify(test_data)


@app.post("/api/v1/test")
def add_test_data():
    if request.is_json:
        response = request.get_json()
        response["id"] = _find_next_id(test_data)
        test_data.append(response)
        # Always best practice to return what was just created
        return response, 201
    return {"error": "Request must be JSON"}, 415


@app.put("/api/v1/test/<int:test_id>")
def edit_test_data(test_id: int):
    if request.is_json:
        data = [data for data in test_data if data['id'] == test_id]
        if len(data) == 0:
            return {"error": f"No data found for ID {test_id}"}, 404
        elif 'name' not in request.json or 'address' not in request.json or 'email' not in request.json:
            return {"error": "Malformed request."}, 400
        else:
            data[0]['name'] = request.json.get('name')
            data[0]['address'] = request.json.get('address')
            data[0]['email'] = request.json.get('email')
            # Always best practice to return the updated data
            return jsonify(data[0]), 200
    return {"error": "Request must be JSON"}, 415

# def edit_test_data(test_id: int):
#     # How would you implement a delete?
#     # What do you return for a successful delete?
#     # What about error cases?

@app.delete("/api/v1/test/<int:test_id>")
def remove_test_data(test_id: int):
	
	for data in test_data:
		if(data["id"] == test_id):		
			test_data.remove(data)
			return {"operation complete": "user ID " + str(test_id) + " has been deleted"}, 200

	return {"error": "Malformed request."}, 400

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
