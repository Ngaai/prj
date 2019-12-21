from main import db


class Sales(db.Model):
    __table_name__ = 'sales'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    inv_id = db.Column(db.Integer, db.ForeignKey('inventories.id'))
    quantity = db.Column(db.Integer, nullable= False)
    created_at = db.Column(db.DateTime, nullable=False)

    def sell(self):
        db.session.add(self)
        db.session.commit()












