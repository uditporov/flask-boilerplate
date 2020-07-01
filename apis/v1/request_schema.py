from jsonschema import Draft4Validator
from jsonschema.exceptions import ValidationError
from flask_restplus._http import HTTPStatus
from flask_restplus.model import ModelBase, RE_REQUIRED
from flask_restplus import fields, reqparse, inputs
from flask_restplus.errors import abort

from apis.v1 import api
from errors import PayloadValidationErrorCodes


EMAIL_REGEX = r'\S+@\S+\.\S+'
BLANK_EMAIL_REGEX = r'\S+@\S+\.\S+'
STR_REGEX = r'^[^\s]+(\s+[^\s]+)*$'
BLANK_STR_REGEX = r'^$|^[^\s]+(\s+[^\s]+)*$'
NUMBER_REGEX = r'^[0-9]+$'
ALPHANUMERIC_REGEX = r'^[0-9a-zA-Z]+$'
BLANK_NUMBER_REGEX = r'^$|^[0-9]+$'


def validate(self, data, resolver=None, format_checker=None):
    validator = Draft4Validator(self.__schema__, resolver=resolver, format_checker=format_checker)
    try:
        validator.validate(data)
    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST,
              success=False,
              data=[],
              _metadata={},
              message='Input payload validation failed',
              errors=list(format_error(e) for e in validator.iter_errors(data)))


def format_error(error):
    path = list(error.path)
    if error.validator == 'required':
        name = RE_REQUIRED.match(error.message).group('name')
        path.append(name)
    field = '.'.join(str(p) for p in path)
    validator = error.validator
    value = error.validator_value
    error_data = PayloadValidationErrorCodes[validator].value
    error_message = error_data['error_message'].format(**{
        'field': field,
        'value': value
    })
    error_code = error_data['error_code']
    return {
        'error_code': error_code,
        'error_message': error_message
    }


ModelBase.validate = validate
