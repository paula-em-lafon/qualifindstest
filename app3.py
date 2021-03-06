from flask import Flask, request, jsonify, abort
from tree1 import AVLTree
from tree2 import AVLTree2

app = Flask(__name__)

keyvalue= {}
quicktrees ={}
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
                value = keyvalue[data["key"]].maximum(keyvalue[data["key"]].root)
            # if the key and version are availalbe return them
            else:
                if keyvalue[data["key"]].searchTree(data["version"]):
                    value = keyvalue[data["key"]].searchTree(data["version"])
                # if key and version are not available
                else:
                # filter for values smaller than key
                    largest_version = keyvalue[data["key"]].\
                        findlargestleft(data["version"], keyvalue[data["key"]].root)
                    # if the value doesn't exist return an error
                    if largest_version == None:
                        abort(404, "the key, version pair is not available")
                    # if value smaller exists return
                    else:
                        value = largest_version
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
            keyvalue[data["key"]]= AVLTree2()
            keyvalue[data["key"]].insert(current_version, data["value"])
            quicktrees[data["key"]]= AVLTree()
            quicktrees[data["key"]].insert(data["value"])
            resp_val = {"key": data["key"], "value": data["value"], "version": current_version}

        # If key exists
        elif data["key"] in keyvalue:
            # check for if the key contains the value we have provided
            if quicktrees[data["key"]].searchTree(data["value"]):
                # check if the data exists in subsequent key versions
                # if not add it to the current key version
                keyappend = 1
                while True:
                    keyappstr = str(keyappend)
                    if not keyvalue.get(data["key"] + keyappstr):
                        keyvalue[data["key"] + keyappstr]= AVLTree2()
                        keyvalue[data["key"] + keyappstr].insert(current_version, data["value"])
                        quicktrees[data["key"] + keyappstr]= AVLTree()
                        quicktrees[data["key"]+ keyappstr].insert(data["value"])
                        break
                    elif quicktrees[data["key"]+ keyappstr].searchTree(data["value"]) == None:
                        keyvalue[data["key"] + keyappstr].insert(current_version, data["value"])
                        quicktrees[data["key"]+ keyappstr].insert(data["value"])
                        break
                    keyappend += 1
                resp_val = {"key": data["key"] + keyappstr, "value": data["value"],\
                     "version": current_version}
            # if value doesn't exist in key being searched add the value along with
            # the corresponding version number
            else:
                keyvalue[data["key"]].insert(current_version, data["value"])
                quicktrees[data["key"]].insert(data["value"])
                resp_val = {"key": data["key"], "value": data["value"],\
                     "version": current_version}
        # add response value and return
        resp = jsonify(resp_val)
        resp.status_code = 200
        return resp

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400