import logging
from app import db
from flask import jsonify,  Response
from dataclasses import dataclass
from enum import Enum


@dataclass
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def __init__(self, _id, username: str, password: str):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def get_admin(cls) -> 'User':
        if cls.query.first():
            return cls.query.first()
        else:
            logging.info(msg="Creating default admin user.")
            cls.create_user('admin', 'admin')
        return cls.query.first()

    @classmethod
    def create_user(cls, username, password):
        new_user = cls(None, username, password)

        db.session.add(new_user)
        db.session.commit()
        logging.log(level=logging.INFO, msg=f"A user has been added to the database with id {new_user.id}")

    @classmethod
    def delete_user_by_id(cls, _id: int):
        user = cls.query.filter_by(id=_id).first()
        db.session.delete(user)
        db.session.commit()
        logging.warning(f'A user by id {_id} has been deleted from the database')


class InputType(Enum):
    TEXT = 1
    NUMBER = 2
    DATE_PICKER = 3
    CHECKBOX = 4
    DROPDOWN = 5


@dataclass
class FormElement(db.Model):
    __tablename__ = 'form_element'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    input_type = db.Column(db.Integer)
    copyable = db.Column(db.Boolean, default=False)
    compulsory = db.Column(db.Boolean, default=False)

    def __init__(self, name: str, input_type: InputType, copyable=False):
        self.name = name
        self.input_type = input_type.value
        self.copyable = copyable
        logging.info(f"Form element created. ID: {self.id}")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'input_type': self.input_type,
            'copyable': self.copyable,
            'compulsory': self.compulsory,
        }

    @classmethod
    def get_all_form_elements(cls) -> list['FormElement']:
        return cls.query.all()

    @classmethod
    def add_form_element(cls, name: str, input_type: InputType, copyable=False) -> tuple[Response, 'FormElement']:
        if not name or not input_type:
            return jsonify({"success": False, "message": "Geçersiz veri. Lütfen tüm alanları doldurun."}), 400

        new_element = cls(name, input_type, copyable)
        db.session.add(new_element)
        db.session.commit()
        logging.info(msg=f"A new form element has been added to the database with id {new_element.id}")

        return jsonify({"success": True, "message": "Form element successfully added"}), new_element

    @classmethod
    def delete_form_element_by_id(cls, _id: int) -> Response:
        element: FormElement = cls.query.filter_by(id=_id).first()
        if element.input_type == InputType.DROPDOWN:
            DropdownOption.delete_options_of_dropdown(element.id)

        db.session.delete(element)
        db.session.commit()
        logging.warning(f"A form element by id {_id} has been deleted from the database")

        return jsonify({"success": True, "message": "Form element successfully deleted"})


@dataclass
class Form(db.Model):
    __tablename__ = 'form'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    value = db.Column(db.String(6000))

    def __init__(self, value: str, name: str):
        self.name = name
        self.value = value
        logging.info(f"New form created. ID: {self.id}")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
        }

    @classmethod
    def update_value(cls, form_id: int, new_value: str) -> Response:
        form = cls.query.get(form_id)
        if form:
            form.value = new_value
            db.session.commit()
            logging.info(f"Form ID {form_id} updated with new value.")
            return jsonify({"success": True, "message": "Form value successfully updated"})
        else:
            logging.warning(f"Form ID {form_id} not found.")
            return jsonify({"success": False, "message": "No such form found"})

    @classmethod
    def update_name(cls, form_id: int, new_name: str) -> Response:
        form = cls.query.get(form_id)
        if form:
            form.name = new_name
            db.session.commit()
            logging.info(f"Form ID {form_id} updated with new name.")
            return jsonify({"success": True, "message": "Form name successfully updated"})
        else:
            logging.warning(f"Form ID {form_id} not found.")
            return jsonify({"success": False, "message": "No such form found"})

    @classmethod
    def add_form(cls, value: str, name: str = None) -> Response:
        new_form = cls(value, name)
        db.session.add(new_form)
        db.session.commit()
        logging.info(msg=f"A new form has been added to the database with id {new_form.id}")

        return jsonify({"success": True, "message": "Form successfully added"})

    @classmethod
    def get_all_forms(cls) -> list['Form']:
        return cls.query.all()

    @classmethod
    def get_form_by_id(cls, form_id: int) -> 'Form':
        form = cls.query.get(form_id)
        if form:
            logging.info(f"Form ID {form_id} retrieved successfully.")
            return jsonify({"success": True, "data": form.to_dict()})
        else:
            logging.warning(f"Form ID {form_id} not found.")
            return jsonify({"success": False, "message": "Form not found"})


@dataclass
class DropdownOption(db.Model):
    __tablename__ = 'dropdown_option'

    id = db.Column(db.Integer, primary_key=True)
    option_name = db.Column(db.String(160))
    option_element_id = db.Column(db.Integer)

    def __init__(self, option_name: str, option_element_id: int):
        self.option_name = option_name
        self.option_element_id = option_element_id
        logging.info(f"New dropdown option created. ID: {self.id}")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'option_name': self.option_name,
            'option_element_id': self.option_element_id,
        }

    @classmethod
    def get_options_of_dropdown_element(cls, dropdown_element_id: int) -> list['DropdownOption']:
        return cls.query.filter_by(option_element_id=dropdown_element_id).all()

    @classmethod
    def add_new_option(cls, option_name: str, option_element_id: int) -> Response:
        new_option = cls(option_name, option_element_id)

        db.session.add(new_option)
        db.session.commit()
        logging.info(msg=f"A new dropdown has been added to the database with id {new_option.id}")

        return jsonify({"success": True, "message": "Dropdown option successfully added"})

    @classmethod
    def delete_options_of_dropdown(cls, option_element_id: int) -> Response:
        options_to_delete = cls.query.filter_by(option_element_id=option_element_id).all()

        if options_to_delete:
            for option in options_to_delete:
                db.session.delete(option)
            db.session.commit()
            logging.info(f"Deleted {len(options_to_delete)} options for dropdown element ID: {option_element_id}")

            return jsonify({"success": True, "message": "Options successfully deleted from database"})

        return jsonify({"success": False, "message": f"No option found for this ID: {option_element_id}"})
