from flask import Flask, request, jsonify, abort

app = Flask(__name__)

keyvalue= {}
    #'whateverKey': {1: 200, 2: 500, 3: 600, 6: 550}, 'superImportantKey': {4: 1200, 5: 1500}}
current_version = 0

@app.route("/api/v1/", methods=['GET', 'PUT'])
def keys():
    global current_version
    if request.method == 'GET':
        data = request.get_json()
        # error if request not complete
        if 'key' not in data:
            abort(400, "bad request, it must have 'key' or 'key' and 'version'' fields")
        # check if key exists
        if data["key"] not in keyvalue:
            abort(404, "the key is not available")
        else:
            # if there's no version in the request get the largest version
            if 'version' not in data:
                value = keyvalue[data["key"]][max(keyvalue[data["key"]])]
            # if the key and version are availalbe return them
            else:
                if data['version'] in keyvalue[data["key"]]:
                    value = keyvalue[data['key']][data["version"]]
                # if key and version are not available
                else:
                # filter for values smaller than key
                    filteredDict = dict(filter(lambda elem: elem[0] <= data["version"],\
                         keyvalue[data["key"]].items()))
                    # if the value doesn't exist return an error
                    if not filteredDict:
                        abort(404, "the key, version pair is not available")
                    # if value smaller exists return
                    else:
                        value = filteredDict[max(filteredDict)]
            # add response value and return
            resp_val = {"value": value}
            resp = jsonify(resp_val)
            resp.status_code = 200
            return resp

    #the put method 
    elif request.method == 'PUT':
        data = request.get_json()
        # error request not complete
        if 'key' not in data or 'value' not in data:
            abort (400, "bad request, it must have 'key' and 'value' fields")
        current_version += 1
        
        # if the key doesn't exist create it along with the entry
        if data["key"] not in keyvalue:
            keyvalue[data["key"]]={current_version: data["value"]}
            resp_val = {"key": data["key"], "value": data["value"], "version": current_version}

        # If key exists
        elif data["key"] in keyvalue:
            # check for if the key contains the value we have provided
            if data["value"] in keyvalue[data["key"]].values():
                # check if the data exists in subsequent key versions
                # if not add it to the current key version
                keyappend = 1
                while True:
                    keyappstr = str(keyappend)
                    if not keyvalue.get(data["key"] + keyappstr):
                        keyvalue[data["key"]+ keyappstr] = {current_version: data["value"]}
                        break
                    elif not data["value"] in keyvalue[data["key"] + keyappstr].values():
                        keyvalue[data["key"] + keyappstr][current_version] = data["value"]
                        break
                    keyappend += 1
                resp_val = {"key": data["key"] + keyappstr, "value": data["value"],\
                     "version": current_version}
            # if value doesn't exist in key being searched add the value along with
            # the corresponding version number
            else:
                keyvalue[data["key"]][current_version] = data["value"]
                resp_val = {"key": data["key"], "value": data["value"],\
                     "version": current_version}
        # add response value and return
        print(keyvalue)
        resp = jsonify(resp_val)
        resp.status_code = 200
        return resp

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400