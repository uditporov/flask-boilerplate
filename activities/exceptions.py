class ExceptionBase(Exception):
    error_enum = None

    def __init__(self, error_code, message_params_dict={}, *args):
        self.error_enum = error_code
        self.error_code = error_code.name
        self.error_message = error_code.value.format(**message_params_dict)
        super(ExceptionBase, self).__init__(self.error_message, *args)
