from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect


from helper import UserData

"""creating class that will process data and send request to another server"""
user_data = UserData()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'helloworld'
CSRFProtect(app)


@app.route("/")
def homepage():
    """Show homepage."""
    return render_template("index.html")


@app.route("/api/get-lucky-num", methods=["POST"])
def get_lucky_num():

    """receiving data from the user"""
    json_data = request.json.get('$json')

    """checking user data and raising flag to False if data are not correct"""
    data, flag = user_data.check_user_data(json_data)

    """if flag False send note to the user"""
    if not flag:
        json_resp = jsonify(resp=data)
        return json_resp, 201
    
    """sending data to the other server"""
    class_resp = user_data.send_request_to_the_server()
    
    """checking if server correctly responded. If not sending note to the user"""
    if class_resp[0] == 'server error':
        data = [{'status': False}, {'server': 'server error'}]
        json_resp = jsonify(resp=data)
        return json_resp, 201
        
    """sending result to the user"""
    json_resp = jsonify(resp=class_resp)
    return json_resp, 201
    






