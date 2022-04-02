from db import db


class ProductModel(db.Model):
    """Product Model"""

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.Float(precision=2))
    weight = db.Column(db.String(50))
    units = db.Column(db.String(50))
    featured = db.Column(db.Boolean)
    discount = db.Column(db.Float(precision=2))
    # image = db.Column(db.LargeBinary)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('CategoriesModel')

    def __init__(self, name, description,
                 price, category_id, weight,
                 units, featured, discount,
                 ):
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.weight = weight
        self.units = units
        self.featured = featured
        self.discount = discount
        # self.image = image

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category_id,
            "weight": self.weight,
            "units": self.units,
            "featured": self.featured,
            "discount": self.discount,
            # "image": self.image
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_category(cls, category_id):
        return cls.query.filter_by(category=category_id).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
