from flask import Flask, make_response, jsonify, request
import logging
from datetime import datetime
from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range

logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)


class CreateStockOrderSchema(Schema):
    """ /orders - POST

    Parameters:
     - isin (str)
     - limit_price (float)
     - side (str)
     - valid_until (time)
     - quantity (int)
    """
    isin = fields.Str(required=True, validate=Length(equal=12, error='Value length must be exactly 12.'))
    limit_price = fields.Float(required=True,
                               validate=Range(min=0, min_inclusive=False, error='Value must be greater than 0'))
    side = fields.Str(required=True)
    valid_until = fields.Int(required=True)
    quantity = fields.Int(required=True,
                          validate=Range(min=1, min_inclusive=False, error='Value must be greater than 0'))

    @validates('valid_until')
    def is_valid_time_from_timestamp(self, value):
        try:
            time = int(value)
            datetime.utcfromtimestamp(time)
        except Exception as e:
            raise ValidationError("Value is not a correct UTC timestamp")

    @validates('side')
    def is_enum_case_insensitive(self, value):
        if str(value).lower() not in ['buy', 'sell']:
            raise ValidationError("Value must be 'buy' or 'sell'")


create_stock_schema = CreateStockOrderSchema()


def create_stock():
    """
    create stock order
    """
    pass


@app.route('/orders', methods=['POST'])
def process_files():
    response = {
        'success': True,
        'message': 'order created successfully'
    }
    try:
        errors = create_stock_schema.validate(request.form)
        if errors:
            logging.error(str(errors))
            response['success'] = False
            response['message'] = 'request validation error(s)'
            response['body'] = {'errors': errors}
        create_stock()
    except Exception as exc:
        logging.exception(exc)
        response['success'] = False
        response['message'] = 'error occurred while creating order'

    return make_response(jsonify(response), 200)
