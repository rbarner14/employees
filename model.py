"""Flask model for API demo.

Adds Employee and Department models (a department has many
employees).

Both models have a `to_dict()` methods that returns a
copy of the employee or department as a simple dictionary.

Includes function to create several sample departments and
employees.

"""


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(db.Model):
    """Employee."""

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(20),
                     nullable=False,
                     unique=True)

    state = db.Column(db.String(2),
                      nullable=False,
                      default='CA')

    dept_code = db.Column(db.String(5),
                          db.ForeignKey('department.dept_code'))

    dept = db.relationship('Department')

    def __repr__(self):
        return "<Employee id=%d name=%s>" % (
            self.id, self.name)

    def to_dict(self):
        """Turn an employee object into a dictionary."""

        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'dept_code': self.dept_code,
        }


class Department(db.Model):
    """Department. A department has many employees."""

    dept_code = db.Column(db.String(5),
                          primary_key=True)

    dept = db.Column(db.String(20),
                     nullable=False,
                     unique=True)

    phone = db.Column(db.String(20))

    employees = db.relationship('Employee')

    def __repr__(self):
        return "<Department id=%s name=%s>" % (
            self.dept_code, self.dept)


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty existing data
    Employee.query.delete()
    Department.query.delete()

    # Reset PostgreSQL sequence:
    # Now we'll start adding employees with ID #1
    db.session.execute(
        "SELECT setval('employee_id_seq', 1, false)")

    # Add sample employees and departments
    df = Department(dept_code='fin',
                    dept='Finance',
                    phone='555-1000')

    dl = Department(dept_code='legal',
                    dept='Legal',
                    phone='555-2222')

    dm = Department(dept_code='mktg',
                    dept='Marketing',
                    phone='555-9999')

    leonard = Employee(name='Leonard', dept=dl)
    liz = Employee(name='Liz', dept=dl)
    maggie = Employee(name='Maggie', dept=dm)
    nadine = Employee(name='Nadine')

    db.session.add_all(
        [df, dl, dm, leonard, liz, maggie, nadine])
    db.session.commit()


def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///emps'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

    # Create table and fill DB with example data
    db.create_all()
    example_data()
