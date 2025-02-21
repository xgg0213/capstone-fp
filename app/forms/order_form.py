from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, StringField
from wtforms.validators import DataRequired, NumberRange

class OrderForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    side = StringField('Side', validators=[DataRequired()])
    quantity = FloatField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=0.000001)
    ])
    limit_price = FloatField('Limit Price')  # Optional, only for limit orders 