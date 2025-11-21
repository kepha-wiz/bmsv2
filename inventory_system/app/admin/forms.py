from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, DateField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError
from app.models import Product

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    sku = StringField('SKU', validators=[DataRequired()])
    cost_price = FloatField('Cost Price', validators=[DataRequired(), NumberRange(min=0)])
    selling_price = FloatField('Selling Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity_in_stock = IntegerField('Initial Stock', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Category', choices=[
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Food', 'Food & Beverages'),
        ('Office Supplies', 'Office Supplies'),
        ('General', 'General')
    ], default='General')
    description = TextAreaField('Description')
    low_stock_threshold = IntegerField('Low Stock Threshold', validators=[DataRequired(), NumberRange(min=1)], default=10)
    submit = SubmitField('Add Product')
    
    def validate_sku(self, sku):
        product = Product.query.filter_by(sku=sku.data).first()
        if product:
            raise ValidationError('SKU already exists. Please use a different SKU.')
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional
from app.models import Product

class StockAdditionForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity to Add', validators=[DataRequired(), NumberRange(min=1)])
    cost_price = FloatField('New Cost Price (Optional)', validators=[Optional(), NumberRange(min=0)])
    selling_price = FloatField('New Selling Price (Optional)', validators=[Optional(), NumberRange(min=0)])
    reason = StringField('Reason for Price Change (Optional)', validators=[Optional()])
    submit = SubmitField('Add Stock')
    
    def __init__(self, *args, **kwargs):
        super(StockAdditionForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(p.id, f"{p.name} ({p.sku}) - Current: UGX{p.cost_price:.2f}/UGX{p.selling_price:.2f}") 
                               for p in Product.query.order_by(Product.name).all()]

class ReportForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Generate Report')
