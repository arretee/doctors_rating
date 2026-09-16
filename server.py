from flask import Flask, render_template, redirect, session, request

import firebase
import user

server = Flask(__name__)
user_object = user.User()


@server.route("/", methods = ["POST", "GET"])
def route_index():
    """ Main route parser

    Returns:
        flask command: flask command with html or redirect
    """
    if request.method == "POST":
        return redirect("/")
        
    else:
        
        return render_template("index.html", doctors=firebase.get_all_doctors_rates())
    
    
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
        
        
        status = user_object.auth_try(login, password)
        
        if status == True:
            return redirect("/")
        
        else:
            return render_template("login.html", error = True, error_message = "Authentication failed")
            
    
    else:
        login = request.form.get("username_input")
        return redirect("/")
    
    
@server.route("/register", methods= ["POST", "GET"])
def route_register():
    return render_template("register.html")

@server.route("/register_submit", methods=["POST", "GET"])
def route_register_submit():
    if request.method == "POST":
        login = request.form.get("username_input")
        password = request.form.get("password_input")
        password_confirm = request.form.get("password_confirm_input")
        
        status = user_object.register_user(login, password, password_confirm)
        
        if status == True:
            return redirect("/")
        
        else:
            return render_template("register.html", error = True, error_message = status)
            
        
    
    else:
        login = request.form.get("username_input")
        return redirect("/")




if __name__ == '__main__':
    server.run(debug=True)