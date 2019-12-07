import sys
from flask import Flask
from flask import Request
from flask import Response
import MySQLdb

class Handle:

    def __init__(self):
        self.name = sys.argv[1]
    



handler = Handle()

def get_name():
    return handler.name

app = Flask(get_name())

@app.route('/service', methods = ['POST'])
def service_handle():
    f = open("/tmp/script.txt", "r")
    print(f.read())
    return {"code": 200, "message": "success"}

app.run(host='0.0.0.0', port=9090)
