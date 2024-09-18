import logging
from app import db
from flask import jsonify
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
        }

    @classmethod
    def get_all_form_elements(cls) -> list['FormElement']:
        return cls.query.all()

    @classmethod
    def add_form_element(cls, name: str, input_type: InputType):
        if not name or not input_type:
            return jsonify({"success": False, "message": "Geçersiz veri. Lütfen tüm alanları doldurun."}), 400

        new_element = cls(name, input_type)
        db.session.add(new_element)
        db.session.commit()
        logging.info(msg=f"A new form element has been added to the database with id {new_element.id}")

        return jsonify({"success": True, "message": "Form element successfully added"})

    @classmethod
    def delete_form_element_by_id(cls, _id: int):
        element = cls.query.filter_by(id=_id).first()
        db.session.delete(element)
        db.session.commit()
        logging.warning(f"A form element by id {_id} has been deleted from the database")

        return jsonify({"success": True, "message": "Form element successfully deleted"})


@dataclass
class Form(db.Model):
    __tablename__ = 'form'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    value = db.Column(db.String(1500))

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
    def update_value(cls, form_id: int, new_value: str):
        form = cls.query.get(form_id)
        if form:
            form.value = new_value
            db.session.commit()
            logging.info(f"Form ID {form_id} updated with new value.")
        else:
            logging.warning(f"Form ID {form_id} not found.")

    @classmethod
    def add_form(cls, value: str, name: str = None):
        new_form = cls(value, name)
        db.session.add(new_form)
        db.session.commit()
        logging.info(msg=f"A new form has been added to the database with id {new_form.id}")

        return jsonify({"success": True, "message": "Form successfully added"})
