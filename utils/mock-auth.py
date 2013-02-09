import requests, json

actions = {
    'login': [ 'username', 'password' ],
    'logout': [ 'auth_token' ],
}

action = raw_input('Action %r: ' % actions.keys()).strip()
assert action in actions

url = 'http://localhost:5000/' + action
request_headers = {'Content-Type': 'application/json'}
request_data = {}

for param in actions[action]:
    value = raw_input('Param %r: ' % param).strip()
    request_data[param] = value

r = requests.post(
    url,
    data=json.dumps(request_data),
    headers=request_headers)
print r.text
