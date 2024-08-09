"""
Data model which will represent the database tables
"""
from common.customTypes import UserType
from sqlalchemy import Enum

from database import db


class Vendor(db.Model):
    """
    Vendor here represents the company which will use our services
    """
    __tablename__ = "vendors"

    id = db.Column("id", db.Integer, primary_key=True, index=True)
    name = db.Column("name", db.String, nullable=False)
    official_email = db.Column("official_email", db.String, nullable=False)
    address = db.Column("address", db.String, nullable=False)
    business_type = db.Column("business_type", db.String, nullable=False)
    # TODO: Get the allowed business types and make an Enum - B2B & B2C
    domain_name = db.Column("domain_name", db.String, unique=True, nullable=False)
    GSTIN = db.Column("GSTIN", db.String, unique=True, nullable=False)


class User(db.Model):
    """
    The common User table which will have the record for all the possible users of the system
    """
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True, index=True)
    username = db.Column("username", db.String, unique=True, index=True, nullable=False)
    password = db.Column("password", db.Text, nullable=False)
    user_type = db.Column("user_type", Enum(UserType), nullable=False)
    is_active = db.Column("is_active", db.Boolean,  nullable=False)
    vendor_id = db.Column("vendor_id", db.Integer, db.ForeignKey("vendors.id"))
    # vendors = db.relationship("Vendor", back_populates="vendors")
