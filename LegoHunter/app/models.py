from . import db


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    set_number = db.Column(db.Integer, nullable=False)
    site = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(2047), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_modified = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f"<Item {self.title}>"
