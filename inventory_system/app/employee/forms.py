from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from app.models import Product

class SaleForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Record Sale')
    
    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(p.id, f"{p.name} ({p.sku}) - ${p.selling_price:.2f} - Stock: {p.quantity_in_stock}") 
                               for p in Product.query.filter(Product.quantity_in_stock > 0).all()]