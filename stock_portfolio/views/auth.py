from flask import Blueprint
from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError

from stock_portfolio.data_access.user import register_user
from stock_portfolio.data_access.user import register_user
from stock_portfolio.data_access.user import UserAlreadyExistsException
from stock_portfolio.util.auth import InvalidLoginCredentialsException
from stock_portfolio.util.auth import validate_login_credentials

# Defining a blue print for all URLs that begin with /auth.
# All views that are related to auth should be registered with
# this blueprint and this blueprint will in turn be registred
# with the flask application
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Case: When the register view is called with HTTP GET, we return
    # a form where the user can enter their username and password
    if request.method == 'GET':
        return render_template('auth/register.html')

    # Case: When the register view is called with HTTP POST, we try to
    # register them in the database
    else:
        # request.form is a special type of dict mapping submitted form keys
        # and values.
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            raise BadRequest('Username and password are required fields')

        # Attempt to register the user and return the appropriate response
        # to the client
        try:
            user = register_user(username, password)
        except UserAlreadyExistsException:
            return {
                'status_code': 200,
                'error': 'Username has already been taken'
            }
        else:
            if not user:
                raise InternalServerError(f'Could not register {username}')

            return {
                'status_code': 200,
                'username': user.username,
                'password': user.password,
            }


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            raise BadRequest('Username and password are required fields')

        # Retrieve the user's information and set the user id in the
        # session if the login credentials are correct
        try:
            user = validate_login_credentials(username, password)
        except InvalidLoginCredentialsException:
            flash('Invalid Login Credentials')
            return
        else:
            session.clear()
            session.user['user_id'] = user.id
            return redirect(url_for('index'))