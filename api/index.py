import json
from flask import Blueprint, render_template, jsonify, request
from app import get_app
from flask_caching import Cache
from app.models import FormElement, Form, DropdownOption
from calendar_service import authenticate_google_calendar, create_event
from datetime import datetime

service = authenticate_google_calendar()
api_index = Blueprint('api_index', __name__, url_prefix='/')
cache = Cache(get_app(), config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 3
})
cache.init_app(get_app())


@api_index.route('/', methods=['GET'])
@cache.cached()
def index():
    return render_template('index.html', forms=Form.get_all_forms())


@api_index.route('/form/elements', methods=['GET'])
def get_form_elements():
    return jsonify({
        'success': True,
        'data': [element.to_dict() for element in FormElement.get_all_form_elements()]
    })


@api_index.route('/form/add', methods=['POST'])
def add_form():
    data = request.form
    form_elements = {k: v for k, v in data.items() if k != 'formName'}
    form_value = json.dumps(form_elements)

    if data.get('formName'):
        Form.add_form(form_value, data.get('formName'))
    else:
        return jsonify({"success": False, "message": "Form name does not exist"})

    return jsonify({"success": True, "message": "Form successfully added"})


@api_index.route('/form/<int:form_id>', methods=['GET'])
def get_form(form_id: int):
    return Form.get_form_by_id(form_id)


@api_index.route('/form/update/<int:form_id>', methods=['POST'])
def update_form(form_id: int):
    data = request.form
    form_elements = {k: v for k, v in data.items() if k != 'formName'}
    form_value = json.dumps(form_elements)
    Form.update_value(form_id, form_value)

    if data.get('formName'):
        Form.update_name(form_id, data.get('formName'))
    else:
        return jsonify({"success": False, "message": "Form name does not exist"})

    return jsonify({"success": True, "message": "Form successfully added"})


@api_index.route('/dropdown/options/<int:element_id>', methods=['GET'])
def get_dropdown_options(element_id: int):
    options = DropdownOption.get_options_of_dropdown_element(element_id)
    return jsonify({
        'success': True,
        'data': [option.to_dict() for option in options]
    })
