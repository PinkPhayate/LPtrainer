from flaskr import app

@app.route("/")
def hello_world():
    return "hello world!"

if __name__ == '__main__':
    app.run(threaded=True)
