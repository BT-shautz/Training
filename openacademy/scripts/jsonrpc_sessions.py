import json
import random
import urllib.request

HOST = 'localhost'
PORT = 8069
DB = 'training'
USER = 'admin'
PASS = 'admin'

def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type":"application/json",
    })
    r = urllib.request.urlopen(req).read()
    reply = json.loads(r.decode('utf-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

# log in the given database
url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)
print("Logged in as %s (uid: %d)" % (USER, uid))

# Search for Demo User
args = [('name', '=', 'Demo User')]
demo_user_id= call(url, "object", "execute", DB, uid, PASS, 'res.partner',
                   'search', args)
print(demo_user_id)


# 2. Read the sessions
sessions = call(url, "object", "execute", DB, uid, PASS, 'openacademy.session',
                   'search_read', [], ['name','seats'] )
for session in sessions:
    print("Session %s (%s seats)" % (session['name'], session['seats']))

# 3.create a new session
course_id = call(url, "object", "execute", DB, uid, PASS, 'openacademy.course',
                   'search', [('name','ilike', 'Technical Training')])[0]

session_id = call(url, "object", "execute", DB, uid, PASS, 'openacademy.session',
                   'create', { 'name' : 'My session', 'course_id' : course_id,})
