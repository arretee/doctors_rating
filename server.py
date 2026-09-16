from flask import Flask, render_template, redirect, session, request

import firebase

server = Flask(__name__)

doctors = {
    1: {"name" : "artem", "specialization": "sigma"},
    2: {"name" : "anton", "specialization": "alfa"},
    3: {"name" : "gal", "specialization": "gay"},
}

user = {
    "username": "",
    "password": ""
}


@server.route("/", methods = ["POST", "GET"])
def route_index():
    """ Main route parser

    Returns:
        flask command: flask command with html or redirect
    """
    if request.method == "POST":
        return redirect("/")
        
    else:
        return render_template("index.html", doctors=doctors)
    
    
@server.route("/login", methods = ["POST", "GET"])
def route_login():
    """To route login

    Returns:
        render temlple: _description_
    """
    return render_template("login.html")


@server.route("/login_submit", methods = ["POST", "GET"])
def route_login_submit():
    if request.method == "POST":
        login = request.form.get("username_input")
        password = request.form.get("password_input")
        
        
        user = firebase.find_user_by_name(login)
        
        if password == "":
            return render_template("login.html", error = True, error_message = "Enter password")
            
        
        if user == None:
            return render_template("login.html", error = True, error_message = "Account not found")
        
        return redirect("/")
    
    else:
        login = request.form.get("username_input")
        return redirect("/")



if __name__ == '__main__':
    server.run(debug=True)