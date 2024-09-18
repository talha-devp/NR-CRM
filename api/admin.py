import logging
from functools import wraps
from flask import jsonify, Blueprint, request, session, redirect, url_for, render_template
from app.models import User, FormElement, InputType

api_admin = Blueprint('api_admin', __name__, url_prefix='/admin')


def is_authenticated():
    return session.get('authenticated', False)


# Decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            logging.log(level=logging.WARNING, msg="This session is not authorized")
            return redirect(url_for('api_admin.login'))
        return f(*args, **kwargs)

    return decorated_function


@api_admin.route('/', methods=['POST', 'GET'])
def login():
    try:
        try:
            if session['authenticated']:
                return redirect(url_for('api_admin.admin_index'))
        except KeyError:
            pass

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            logging.info("Admin form submitted.")
            admin = User.get_admin()

            if username == admin.username and password == admin.password:
                session['authenticated'] = True
                logging.info("Admin logged in.")
                return redirect(url_for('api_admin.admin_index'))

            logging.error("Invalid credentials")
            return render_template("admin/login.html", message="Invalid credentials"), 401
        return render_template("admin/login.html")
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return jsonify({"success": False, "message": str(e)}), 405


@api_admin.route('/index', methods=['POST', 'GET'])
@login_required
def admin_index():
    form_elements = FormElement.get_all_form_elements()
    return render_template('admin/index.html', form_elements=form_elements, input_types=InputType)


@api_admin.route('/logout', methods=['POST'])
@login_required
def logout():
    logging.info(msg="Logout called")
    session.pop('authenticated', None)
    return jsonify({"successful": True, "message": "Logged out"})


@api_admin.route('/element/add', methods=['POST'])
@login_required
def add_form_element():
    logging.info(msg="Add form element called")
    data = request.get_json()
    print(data)
    name = data.get('name')
    input_type = InputType(int(data.get('input_type')))
    copyable = bool(data.get('copyable'))

    return FormElement.add_form_element(name, input_type, copyable)


@api_admin.route('/element/delete/<int:_id>', methods=['DELETE'])
@login_required
def delete_form_element(_id: int):
    logging.info(msg="Delete form element called")
    return FormElement.delete_form_element_by_id(_id)
