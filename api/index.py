import json
from flask import Blueprint, render_template, jsonify, request
from app import get_app
from flask_caching import Cache
from app.models import FormElement, Form

api_index = Blueprint('api_index', __name__, url_prefix='/')

cache = Cache(get_app(), config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 3
})
cache.init_app(get_app())


@api_index.route('/', methods=['GET'])
@cache.cached()
def index():
    return render_template('index.html', form_elements=FormElement.get_all_form_elements())


@api_index.route('/form/elements', methods=['GET'])
def get_form_elements():
    elements = FormElement.get_all_form_elements()
    return jsonify({
        'success': True,
        'data': [element.to_dict() for element in elements]
    })


@api_index.route('/form/add', methods=['POST'])
def add_form():
    data = request.form
    print(data)
    form_elements = {k: v for k, v in data.items()}
    form_value = json.dumps(form_elements)

    Form.add_form(form_value)

    return jsonify({"success": True, "message": "Form successfully added"})
