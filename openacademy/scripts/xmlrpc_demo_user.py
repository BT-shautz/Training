import xmlrpc.client

HOST = 'localhost'
PORT = 8069
DB = 'training'
USER = 'admin'
PASS = 'admin'

root = 'http://%s:%d/xmlrpc/' % (HOST, PORT)
uid = xmlrpc.client.ServerProxy(root + 'common').login(DB, USER, PASS)
print("Logged in as %s (uid: %d)" % (USER, uid))

# Read Demo User db id
sock = xmlrpc.client.ServerProxy(root + 'object')
args = [('name', '=', 'Demo User')]
demo_user_id= sock.execute(DB, uid, PASS, 'res.partner', 'search', args)
print(demo_user_id)
