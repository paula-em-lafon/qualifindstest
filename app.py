from flask import Flask, request, jsonify, abort

app = Flask(__name__)

keyvalue= []
# {'key': 'whateverKey', 'value': 200, 'version': 1},\
#      {'key': 'whateverKey', 'value': 500, 'version': 2},\
#           {'key': 'whateverKey', 'value': 600, 'version': 3},\
#                {'key': 'superImportantKey', 'value': 1200, 'version': 4},\
#                     {'key': 'superImportantKey', 'value': 1500, 'version': 5},\
#                          {'key': 'whateverKey', 'value': 550, 'version': 6}
current_version = 0

@app.route("/api/v1/", methods=['GET', 'PUT'])
def keys():
    global current_version

    # get request handling
    if request.method == 'GET':
        data = request.get_json()
        if 'key' not in data:
            abort(400, "bad request, it must have 'key' or 'key' and 'version'' fields")
        if 'key' in data and 'version' not in data:
            ready_values = []
            for elem in filter(lambda x: x['key'] == data['key'], keyvalue):
                ready_values.append(elem)
            if ready_values:
                return_value = max(ready_values, key=lambda d: d['version'])
                resp = jsonify({"value":return_value['value']})
                resp.status_code = 200
                return resp
            else:
                abort(404, "the key is not available")
        if 'key' in data and 'version' in data:
            ready_values = []
            for elem in filter(lambda x: x['key'] == data['key']and\
                x['version'] <= data['version'], keyvalue):
                ready_values.append(elem)
            if ready_values:
                return_value = max(ready_values, key=lambda d: d['version'])
                resp = jsonify({"value":return_value['value']})
                resp.status_code = 200
                return resp
            else:
                abort(404, "the key, version pair is not available")
    # Put request handling
    elif request.method == 'PUT':
        data = request.get_json()
        if 'key' not in data or 'value' not in data:
            abort (400, "bad request, it must have 'key' and 'value' fields")
        # if key value pair doesn't exist create a new one
        if not any(d['key'] == data['key'] and d['value'] == data['value'] for d in keyvalue):
            current_version += 1
            new_entry = {"key": data['key'], "value": data['value'], "version": current_version}
            keyvalue.append(new_entry)
            resp = jsonify(new_entry)
            resp.status_code = 200
            return resp
        # if key value pair exists 
        else:
            current_version += 1
            ready_values = []
            keyappend = 1
            while True:
                keyappstr = str(keyappend)
                if not any(d['key'] == data['key'] + keyappstr and \
                    d['value'] == data['value'] for d in keyvalue):
                    new_entry = {"key": data['key'] + keyappstr, \
                        "value": data['value'], "version": current_version}
                    break
                keyappend += 1
            keyvalue.append(new_entry)
            resp = jsonify(new_entry)
            resp.status_code = 200
            return resp

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400