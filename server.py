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

from jinja2 import StrictUndefined

from flask import Flask, jsonify, request, render_template, redirect, flash
from flask_restless import APIManager
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, Employee, Department, db

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/')
def index():

    return render_template("homepage.html")


# @app.route('/api2/employee', methods=['GET'])
# def employee_list():
#     """List employees."""

#     emps = [e.to_dict() for e in Employee.query.all()]
#     return jsonify(employees=emps)


@app.route('/api2/employee', methods=['GET'])
def employee_list():
    """List employees."""

    all_employees = Employee.query.all()
   
    return render_template("employee_list.html",employees=all_employees)


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

@app.route("/add_employee", methods=["GET"])
def employee_add():
    """Show employee registration form."""

    return render_template("add_employee.html")


@app.route("/add_employee", methods=["POST"])
def employee_add_process():
    """Add new user to database."""

    e = Employee(name=request.form['name'],
                 state=request.form['state'],
                 dept_code=request.form['dept_code']
                )

    db.session.add(e)
    db.session.commit()

    flash("Employee added.")

    return redirect("/api2/employee")


# @app.route('/api2/employee/<int:id>', methods=['GET'])
# def employee_detail(id):
#     """Get detail on one employee."""

#     e = Employee.query.get_or_404(id)
#     return jsonify(e.to_dict())


@app.route('/api2/employee/<int:id>', methods=["GET"])
def employee_detail(id):
    """Get detail on one employee."""

    e = Employee.query.get_or_404(id)

    return render_template("employee.html", employee=e)


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
