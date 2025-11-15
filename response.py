from flask import jsonify

# GET, PUT/PATCH, DELETE
def success_response(message:str,data=None):
    """
        Generic success response for GET, PUT/PATCH, DELETE. 
    """


    return jsonify({
        "success":True,
        "message":message,
        "data": data 
    }),200

def not_found(entity:str = "Resource"):
    """
        Generate a standardized 404 not found response
    """
    return jsonify({
        "success":False,
        "message":f"{entity} not found"
    }),404