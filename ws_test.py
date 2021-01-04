import xmlrpc.client

DB = 'demo'
USER = 'admin@mail.com'
PASS = 'admin'
URL = 'http://localhost:8069/xmlrpc/'

uid = xmlrpc.client.ServerProxy(URL + 'common').login(DB, USER, PASS)
print("Logged in as %s (uid:%d)" % (USER, uid))

models = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/object')
results = models.execute_kw(DB, uid, PASS, 'pr.project', 'search_read', [[]], {'limit': 5})
for r in results:
    print(r.get('id'), r.get('name'), r.get('budget'))

ids = [3, 200, 272]
results = models.execute_kw(DB, uid, PASS, 'pr.project', 'name_get', [ids])
for r in results:
    print(r)

id = models.execute_kw(DB, uid, PASS, 'pr.project', 'create', [{
    'name': 'New Name by Webservice',
    'department': 'ICT',
    'budget': 50000,
}])
print(id)

ids = [id]
result = models.execute_kw(DB, uid, PASS, 'pr.project', 'write', [ids, {
    'name': 'New Name by Webservice (Updated)',
}])
print('result=', result)

ids = [id]
result = models.execute_kw(DB, uid, PASS, 'pr.project', 'unlink', [ids])
print('delete result=', result)
