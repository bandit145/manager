from flask import request, Flask

app = Flask(__name__)


# ipam endpoint
@app.route('/v1/ipam', methods=['GET', 'POST', 'DELETE'])
def ipam():
    if request.method == 'POST':
        return ipam_operations.create()
    elif request.method == 'DELETE':
        return ipam_operations.delete()
    elif request.method == 'GET':
        return ipam_operations.query()
