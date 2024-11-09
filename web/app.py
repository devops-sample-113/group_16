from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/admin")
def admin():
    # return admin html page
    return ""