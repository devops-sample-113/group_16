from flask import Flask,render_template
app = Flask(__name__)
@app.route("/")
def hello():
    return render_template('Login.html')
if __name__ == "__main__":
    app.debug = True
    app.run(host='localhost', port=5000)
