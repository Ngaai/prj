
from main import db
from models.sales import Sales


class Inventories(db.Model):
    """dada method"""
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    buying_price = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    sales = db.relationship('Sales', backref='inv', lazy=True)

    """static method -must be in the class"""
    def add_records(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_records(cls):
        return cls.query.all()

    @classmethod
    def fetch_a_record(cls, id1):
        return cls.query.filter_by(id=id1).first()

    def delete_record(self):
        db.session.delete(self)
        db.session.commit()



