"""Flask server that demonstrates serving APIs.

Serves similar same API twice, both by hand and using Flask-restless.

/api : created using Flask-restless
  /api/department/
  /api/employee/

/api2 : created by making routes and doing work directly
  /api2/employee
  (we don't create the /api/department for this version)

Joel Burton <joel@joelburton.com>
"""

# For HTML templating.
from jinja2 import StrictUndefined
# For debugging, receiving/delivering requests, alerts, and form actions.
# To create app.
from flask import Flask, jsonify, request, render_template, redirect, flash
from flask_restless import APIManager
from flask_debugtoolbar import DebugToolbarExtension
# For access to/communicating with database.
from model import connect_to_db, Employee, Department, db
# For url requests
import requests
# For API calls.
from findAVenue import findAVenue
# For secret keys.
import os
# For jQuery adjective component.
import random
# For jQuery adjective component (sleep).
import time

# API Keys.
foursquare_client_id = os.environ.get('FORSQUARE_CLIENT_ID')
foursquare_client_secret = os.environ.get('FORSQUARE_CLIENT_SECRET')
google_api_key = os.environ.get('GOOLE_API_KEY')

# Instantiating Flask app.
app = Flask(__name__)

# Needed for debugging.
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

ADJECTIVES = ['fun', 'fantastic', 'kickass', 'ballerific', 'awesome', 'sweet']


@app.route('/')
def index():

    adjective = random.choice(ADJECTIVES)

    return render_template('homepage.html', adjective=adjective)


# jQuery components are their own routes.
@app.route('/adjective')
def get_random_adjective():
    """Show random adjective."""

    # Simulate a slow server
    time.sleep(2)

    return random.choice(ADJECTIVES)


@app.route('/compliment')
def get_random_compliment():

    time.sleep(2)

    consent = request.args.get("compliment")

    if consent == "Yes":
        return random.choice(["You are smart.", "You are kind.", 
                              "You will change the world for the better!"])
    else:
        return "Okay, maybe tomorrow."


@app.route('/venue_search', methods=['GET'])
def search_venue():
    """Show search box."""

    return render_template('venue_search.html')


@app.route('/venue', methods=['GET'])
def venue_result():

    location = request.args.get('location')

    venue = findAVenue(13, location)

    name = venue['name']
    address = venue['address']
    image = venue['image']

    return render_template('venue.html', name=name, address=address, image=image)



# @app.route('/api2/employee', methods=['GET'])
# def employee_list():
#     """List employees."""

#     emps = [e.to_dict() for e in Employee.query.all()]
#     return jsonify(employees=emps)


@app.route('/api2/employee', methods=['GET'])
def employee_list():
    """List employees."""

    all_employees = Employee.query.all()
   
    return render_template('employee_list.html',employees=all_employees)


@app.route('/employees_in_db.json', methods=['GET'])
def get_employees_in_db():
    """List employees."""

    all_employees = Employee.query.all()

    all_employees_json = {}

    for employee in all_employees:
        all_employees_json[employee.name] = {
            "state": employee.state,
            "dept_code": employee.dept_code
        }
    print(all_employees_json)

    return jsonify(all_employees_json)


# @app.route('/api2/employee', methods=['POST'])
# def employee_add():
#     """Add an employee."""

#     # Values from request, as opposed to request.args.get whose details come
#     # from a form
#     e = Employee(name=request.values.get('name'),
#                  state=request.values.get('state'),
#                  dept_code=request.values.get('dept_code'),
#                  )
#     db.session.add(e)
#     db.session.commit()

#     # Return HTTP status code 201, with body being new ID
#     return str(e.id), 201

@app.route('/add_employee', methods=['GET'])
def employee_add():
    """Show employee registration form."""

    return render_template('add_employee.html')


@app.route('/add_employee', methods=['POST'])
def employee_add_process():
    """Add new user to database."""

    e = Employee(name=request.form['name'],
                 state=request.form['state'],
                 dept_code=request.form['dept_code']
                )

    db.session.add(e)
    db.session.commit()

    # For dramatic pause to emphasize jQuery method happening in back end.
    time.sleep(2)

    # flash('Employee added.')

    # return redirect('/api2/employee')
    return "Employee added."


# @app.route('/api2/employee/<int:id>', methods=['GET'])
# def employee_detail(id):
#     """Get detail on one employee."""

#     e = Employee.query.get_or_404(id)
#     return jsonify(e.to_dict())


@app.route('/api2/employee/<int:id>', methods=['GET'])
def employee_detail(id):
    """Get detail on one employee."""

    e = Employee.query.get_or_404(id)

    return render_template('employee.html', employee=e)


@app.route('/api2/employee/<int:id>', methods=['PUT', 'PATCH'])
def employee_update(id):
    """Update an existing employee."""

    e = Employee.query.get_or_404(id)
    if 'name' in request.values:
        e.name = request.values['name']
    if 'state' in request.values:
        e.state = request.values['state']
    if 'dept_code' in request.values:
        e.dept_code = request.values['dept_code']
    db.session.commit()

    # Return status code 200, with body being ID updated
    return str(id), 200


@app.route('/api2/employee/<int:id>', methods=['DELETE'])
def employee_delete(id):
    """Delete an employee."""

    Employee.query.filter_by(id=id).delete()
    db.session.commit()

    # Return status code 200, with empty body
    return "", 200


if __name__ == '__main__':
    
    app.debug = True

    connect_to_db(app)

    manager = APIManager(app, flask_sqlalchemy_db=db)

    # Create API endpoints, which will be available at /api/<tablename> by
    # default. Allowed HTTP methods can be specified as well.

    manager.create_api(
        Department,
        methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])

    manager.create_api(
        Employee,
        methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])

    app.run(debug=True, host='0.0.0.0')
