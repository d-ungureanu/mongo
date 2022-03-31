from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

###############################################################
app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="localhost",
                                port=27017,
                                serverSelectionTimeoutMS=1000
                                )
    db = mongo.company

    mongo.server_info()  ##trigger exception if can not connect to DB
except:
    print("ERROR - Cannot connect to DB.")


###############################################################
# add to DB
@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Can not read users."}),
            status=500,
            mimetype="application/json"
        )


###############################################################
# list the DB entries
@app.route("/users", methods=["POST"])
def create_user():
    try:
        temp_spartan = request.get_json()
        user = {
            "first_name": temp_spartan["first_name"],
            "last_name": temp_spartan["last_name"],
            "birth_day": temp_spartan["birth_day"],
            "birth_month": temp_spartan["birth_month"],
            "birth_year": temp_spartan["birth_year"],
            "course": temp_spartan["course"],
            "sparta_id": temp_spartan["sparta_id"],
            "stream": temp_spartan["stream"]
        }
        db_response = db.users.insert_one(user)
        print(db_response.inserted_id)
        return Response(
            response=json.dumps({"message": "User created", "id": f"{db_response.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
        # for attr in dir(db_response):
        #     print(attr)
    except Exception as ex:
        print("**********************")
        print(ex)
        print("**********************")


###############################################################
@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        db_response = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"first_name": request.form["first_name"]}}
        )
        if db_response.modified_count == 1:
            return Response(
                response=json.dumps({"message": "User updated."}),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({"message": "Nothing to update."}),
            status=200,
            mimetype="application/json"
        )


    except Exception as ex:
        print("******************************")
        print(ex)
        print("******************************")
        return Response(
            response=json.dumps({"message": "Sorry can not update user."}),
            status=500,
            mimetype="application/json"
        )


###############################################################
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        db_response = db.users.delete_one({"_id": ObjectId(id)})
        if db_response.deleted_count == 1:
            return Response(response=json.dumps({"message": "User deleted", "id": f"{id}"}), status=200, mimetype="application/json")
        return Response(response=json.dumps({"message": "User not found", "id": f"{id}"}), status=200, mimetype="application/json")
    except Exception as ex:
        print("********************")
        print(ex)
        print("********************")
        return Response(
            response=json.dumps({"message": "Sorry can not delete user."}),
            status=500,
            mimetype="application/json"
        )


###############################################################

if __name__ == "__main__":
    app.run(port=8080, debug=True)
