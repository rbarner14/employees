"""Example of using an API."""

import requests
from pprint import pprint


def print_emp(label, api, emp_id):
    """Print detail about an employee."""

    print()
    print(label)
    print()

    emp = requests.get(
        "http://localhost:5000/%s/employee/%s" % (api, emp_id)).json()
    pprint(emp, width=40, indent=2)

    print()
    input("=====")


###########################################################
# Use the auto-built API (/api)

print("\n===========================================")
print("Using Auto-Built API (/api)")

resp = requests.post("http://localhost:5000/api/employee",
                     json={'name': 'Leroy',
                           'state': 'CA',
                           'dept_code': 'legal'})

# This returns the JSON of the new employee; get ID
new_id = resp.json()['id']

print_emp("Show new employee", "api", new_id)

print(requests.patch(
    f'http://localhost:5000/api/employee/{new_id}',
    json={'name': 'Lancelot'}))

print_emp("Show edited employee #5", "api", new_id)

print(requests.delete(
    f'http://localhost:5000/api/employee/{new_id}'))


###########################################################
# Use the handmade API (/api2)

print("\n===========================================")
print("Using Auto-Built API (/api)")

resp = requests.post("http://localhost:5000/api2/employee",
                     {'name': 'Leroy',
                      'state': 'CA',
                      'dept_code': 'legal'})

new_id = resp.text

print_emp("Show new employee", "api2", new_id)

print(requests.patch(
    f'http://localhost:5000/api2/employee/{new_id}',
    {'name': 'Lancelot'}))

print_emp("Show edited employee", "api2", new_id)

print(requests.delete(
    f'http://localhost:5000/api2/employee/{new_id}'))
