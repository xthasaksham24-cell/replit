from datetime import datetime
from app import db
from sqlalchemy import Numeric
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    balance = db.Column(Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    balance = db.Column(Numeric(10, 2), default=0.00)
    tax_number = db.Column(db.String(50))
    discount_rate = db.Column(Numeric(5, 2), default=0.00)
    vat_rate = db.Column(Numeric(5, 2), default=0.00)
    excise_rate = db.Column(Numeric(5, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(50), unique=True, nullable=False)
    product = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    cp = db.Column(Numeric(10, 2), nullable=False)  # Cost Price
    wholesale = db.Column(Numeric(10, 2), nullable=False)
    sp = db.Column(Numeric(10, 2), nullable=False)  # Selling Price
    uom = db.Column(db.String(20), nullable=False)  # Unit of Measure
    opening_quantity = db.Column(Numeric(10, 2), default=0.00)
    current_quantity = db.Column(Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    total_amount = db.Column(Numeric(10, 2), nullable=False)
    discount = db.Column(Numeric(10, 2), default=0.00)
    tax_amount = db.Column(Numeric(10, 2), default=0.00)
    final_amount = db.Column(Numeric(10, 2), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    customer = db.relationship('Customer', backref='sales')
    items = db.relationship('SaleItem', backref='sale', cascade='all, delete-orphan')

class SaleItem(db.Model):
    __tablename__ = 'sale_items'
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(Numeric(10, 2), nullable=False)
    unit_price = db.Column(Numeric(10, 2), nullable=False)
    total_price = db.Column(Numeric(10, 2), nullable=False)
    
    item = db.relationship('Item')

class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    total_amount = db.Column(Numeric(10, 2), nullable=False)
    discount = db.Column(Numeric(10, 2), default=0.00)
    tax_amount = db.Column(Numeric(10, 2), default=0.00)
    final_amount = db.Column(Numeric(10, 2), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    vendor = db.relationship('Vendor', backref='purchases')
    items = db.relationship('PurchaseItem', backref='purchase', cascade='all, delete-orphan')

class PurchaseItem(db.Model):
    __tablename__ = 'purchase_items'
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(Numeric(10, 2), nullable=False)
    unit_price = db.Column(Numeric(10, 2), nullable=False)
    total_price = db.Column(Numeric(10, 2), nullable=False)
    
    item = db.relationship('Item')
