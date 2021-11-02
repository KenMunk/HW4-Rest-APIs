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
	

def get_id(test_id: int, test_list: list, searchID="id"):
    data = -1
    cursor = -1
    
    #looking for the user specified
    for entry in test_list:
        cursor+=1
        if(entry[searchID] == test_id):
            data = cursor
            break
    
    return(data)

def _find_next_id(data_list: list):
    """Small helper function to find the next ID from a previous list of data"""
    return max(data["id"] for data in data_list) + 1
'''
Test data stuffs
'''

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



'''
User Data stuffs
'''

'''
Sample Curl Command:

curl -X GET http://localhost:8080/users/everyone -H "Content-Type:application/json"

'''
@app.get("/users/everyone")
def get_user_data():
    return jsonify(user_data), 200

'''
Sample Curl Command:

curl -X GET http://localhost:8080/users/1 -H "Content-Type:application/json"
curl -X GET http://localhost:8080/users/0 -H "Content-Type:application/json"

'''
@app.get("/users/<int:test_id>")
def get_user_(test_id: int):
    data = get_id(test_id, user_data)
    
    #if the user is found then return the user, otherwise, announce that the request was wrong
    if(not (data == -1)):
        return jsonify(user_data[data]), 200
    else:
        return {"error": "No user found."}, 400

'''
Sample Curl Command:

curl -X POST http://localhost:8080/users -d "{\"name\": \"Jordan Peterson\", \"type\": \"author\"}" -H "Content-Type:application/json"

'''
@app.post("/users")
def add_user_():
    
    if request.is_json:
        if "name" in request.json and "type" in request.json:
            newID = _find_next_id(user_data)
            response = request.get_json()
            response["id"] = newID
            user_data.append(response)
            
            for check in user_data:
                if(check["id"] == newID):
                    return response, 200
            return {"error": "Action failed."}, 400
        else:
            return {"error": "No user found."}, 400
        
        
    
    return {"error": "Request must be JSON"}, 415


'''
Sample Curl Command:

curl -X PUT http://localhost:8080/users/2 -d "{\"name\": \"John Sullivan\", \"type\": \"reader\"}" -H "Content-Type:application/json"

curl -X PUT http://localhost:8080/users/2 -d "{\"name\": \"Johnathen Sullivan\"}" -H "Content-Type:application/json"

curl -X PUT http://localhost:8080/users/2 -d "{\"type\": \"pro_reader\"}" -H "Content-Type:application/json"

'''
@app.put("/users/<int:test_id>")
def edit_user_(test_id: int):

    if request.is_json:
        userID = get_id(test_id, user_data)
        
        #check if the user id is valid
        if(userID == -1):
            return {"error": "No user found."}, 400
        #attempt to do something with the data after validating
        else:
            if "name" in request.json and "type" in request.json:
                user_data[userID]["name"] = request.json["name"]
                user_data[userID]["type"] = request.json["type"]
                return jsonify(user_data[userID]), 200
                
            elif "name" in request.json:
                user_data[userID]["name"] = request.json["name"]
                return jsonify(user_data[userID]), 200
                
            elif "type" in request.json:
                user_data[userID]["type"] = request.json["type"]
                return jsonify(user_data[userID]), 200
                
            else:
                return {"error": "No user found."}, 400
        
    return {"error": "Request must be JSON"}, 415

'''
Sample Curl Command:

curl -X POST http://localhost:8080/users/reset -H "Content-Type:application/json"

'''
@app.post("/users/reset")
def reset_user_data():
    user_data = [
        {"id": 1, "name": "Kane", "type": "admin"},
        {"id": 2, "name": "John", "type": "reader"},
        {"id": 3, "name": "Jim", "type": "author"}
    ]
    return jsonify(user_data), 200

'''
Sample Curl Command:

curl -X DELETE http://localhost:8080/users/2 -H "Content-Type:application/json"

'''
@app.delete("/users/<int:test_id>")
def remove_user_(test_id: int):
    userID = get_id(test_id, user_data)
    if userID > -1:
        user_data.remove(user_data[userID])
        
        return {"operation complete": "user id " + str(test_id) + " deleted"} , 200
    return {"error": "No user found."}, 400


'''
Recipe Data Stuffs
'''

'''
Sample Curl Command:

curl -X GET http://localhost:8080/users/all/recipies -H "Content-Type:application/json"

'''
@app.get("/users/all/recipies")
def get_all_recipies_():
    return jsonify(recipe_data)

'''
Sample Curl Command:

curl -X GET http://localhost:8080/users/1/recipies -H "Content-Type:application/json"

'''
@app.get("/users/<int:test_id>/recipies")
def get_all_recipies_for_user_(test_id: int):
    user_recipies = []
    for recipie in recipe_data:
        if(recipie["user_id"] == test_id):
            user_recipies.append(recipie)
    
    if(len(user_recipies) == 0):
        return {"error": "No data found."}, 400
    return jsonify(user_recipies), 200        

'''
Sample Curl Command:

curl -X POST http://localhost:8080/users/3/recipies -d "{\"steps\": \"chop steak, season steak, grill steak till medium rare, enjoy steak\" }" -H "Content-Type:application/json"

'''
@app.post("/users/<int:test_id>/recipies")
def add_recipie(test_id: int):
    
    if request.is_json:
        if "steps" in request.json:
            if(get_id(test_id, user_data) > -1):
                #print("is this doing anything?")
                nextID = _find_next_id(recipe_data)
                response = request.get_json()
                response["user_id"] = test_id
                response["id"] = nextID
                recipe_data.append(response)
                
                confirmationID = get_id(nextID, recipe_data)
                
                if confirmationID > -1:
                    return jsonify(recipe_data[confirmationID]), 200
                
                return {"error": "Request failed."}, 400
                    
                
            return {"error": "No user found."}, 400
        return {"error": "Malformed request."}, 400
    
    return {"error": "Request must be JSON"}, 415

'''
Sample Curl Command:

curl -X PUT http://localhost:8080/users/3/recipies/1 -d "{\"steps\": \"chop steak, season steak, grill steak till medium rare, enjoy steak\" }" -H "Content-Type:application/json"

'''
@app.put("/users/<int:test_id>/recipies/<int:recipie_id>")
def edit_recipie_(test_id: int, recipie_id: int):
    
    if request.is_json:
        if(get_id(test_id, user_data) > -1):
            if(get_id(recipie_id, recipe_data) > -1):
                if "steps" in request.json:
                    response = request.get_json()
                    recipe_data[get_id(recipie_id, recipe_data)]["steps"] = response["steps"]
                    return jsonify(recipe_data[get_id(recipie_id, recipe_data)]), 200
                return {"error": "No steps found."}, 400
            return {"error": "No recipe found."}, 400
        return {"error": "No user found."}, 400
        
    return {"error": "Request must be JSON"}, 415

'''
Sample Curl Command:

curl -X DELETE http://localhost:8080/users/1/recipies/1 -H "Content-Type:application/json"

'''
@app.delete("/users/<int:test_id>/recipies/<int:recipie_id>")
def remove_recipie_(test_id: int, recipie_id: int):
    if(get_id(test_id, user_data) > -1):
        if(get_id(recipie_id, recipe_data) > -1):
            data_to_remove = recipe_data[get_id(recipie_id,recipe_data)]
            if(data_to_remove["user_id"] == test_id):    
                recipe_data.remove(data_to_remove)
                return {"operation successful": "recipe " + str(recipie_id) + " from user " + str(test_id) + " has been deleted"}, 200
            return {"error": "No valid recipe found."}, 400
        return {"error": "No recipe found."}, 400
    return {"error": "No user found."}, 400

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
