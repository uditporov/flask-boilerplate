import abc


class ValidatorBase(object):
    """
    Base validator class
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, context, user_uuid, request_id):
        """
        Args:
            All required data should be included in context(dict)
            List all required context attributes here.
        Raises:
            List all Raised error here.
        Side-effects:
            List all other changes like context attributes it sets
            upon successful validation
        Returns:
            Should not return anything. Just raise error in case of failure.
        """
        self.context = context
        self.user_uuid = user_uuid
        self.request_id = request_id

    @abc.abstractmethod
    def validate(self, *args, **kwargs):
        """
        override this method to write validation logic
        :return:
        """
        raise NotImplementedError('Validate not implemented')
