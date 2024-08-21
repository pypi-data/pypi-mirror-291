import re
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, validates
from flask_appbuilder import Model


class Client(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    address = Column(String(564), default="Street ")
    city = Column(String(564))
    state = Column(String(564))
    phone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey("contact_group.id"))
    contact_group = relationship("ContactGroup")


class ContactGroup(Model):
    """
    ContactGroup model representing a group of contacts.

    Attributes:
        id (int): The primary key of the contact group.
        name (str): The name of the contact group.

    Methods:
        __repr__: Returns the name of the contact group.
    """

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Contact(Model):
    """
    Contact model representing a contact with personal information.

    Attributes:
        id (int): The unique identifier for the contact.
        name (str): The name of the contact.
        address (str): The address of the contact.
        birthday (Date): The birthday of the contact.
        email (str): The email of the contact.
        personal_phone (str): The personal phone number of the contact.
        personal_cellphone (str): The personal cellphone number of the contact.
        contact_group_id (int): The foreign key referencing the contact group.
        contact_group (relationship): Relationship with the ContactGroup model.

    Methods:
        __repr__: Returns the name of the contact.
    """

    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    address = Column(String(564), default="Street ")
    birthday = Column(Date)
    email = Column(String(100), unique=True)
    personal_phone = Column(String(20))
    personal_cellphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey("contact_group.id"))
    contact_group = relationship("ContactGroup")

    @validates("email")
    def validate_email(self, key, email):
        if not email:
            raise AssertionError("No email provided")
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError("Provided email is not an email address")
        return email

    def __repr__(self):
        return self.name
