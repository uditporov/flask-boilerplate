from abc import ABC, abstractmethod
from activities.exceptions import ExceptionBase
from activities.exceptions import ActivityMisConfigured
from commons.response import Response
from commons.errors import Error
from errors import ActivityErrorCodes


class ActivityBase(ABC):
    """
    Base class for all the activities, defining the sequence of execution and controlling the
    validations and response structures.
    """

    context_class = None
    """Holds the reference to the context object class"""

    configuration_validators = ()
    """Consists of validators which validates only configuration related values of the request"""

    payload_validators = ()  # TODO: think of a better name
    """Consists of validators which validates only payload/data related values of the request"""

    publishing_topics = ()
    """Consisting of topics to which we need to publish the payload if the activity is completed successfully"""

    #  TODO: handle the updates for elastic search here as well.

    def __init__(self, user_uuid, request_id, *args, **kwargs):
        """
        Initializing the response and other objects
        Note - If any other attribute is to be added in the instance then override this and call super().__init__()
        """
        self.user_uuid = user_uuid
        self.request_id = request_id
        self.response = Response()
        self.context = None
        self.payload = {}

        if not self.context_class:
            raise ActivityMisConfigured(ActivityErrorCodes.ACTIVITY_MISCONFIGURED_ATTRIBUTE,
                                        {"attribute_name": "context_class"})

    def execute(self, payload={}, **kwargs):
        """
        This method controls the sequential execution of each step for the activity.
        Executing the validations first and then the execute part.

        :param payload: Dictionary consisting of payload present in the request directly passed after serialization
        :return:
        """
        self.payload = payload
        # sets the self.context attribute by fetching data from the payload dictionary
        self._set_context(payload, **kwargs)

        # validates the payload based on the validators defined above in the tuples
        self._validate()

        # if validations passed then execute the activity and no error is raised by validator
        if not self.response.errors:
            self._execute()

        if not self.response.errors:
            self._publish_to_topics()

        return self.response

    def _set_context(self, payload, **kwargs):
        """
        Simply sets the context object as per the payload passed to it
        :param payload:
        :return:
        """
        self.context = self.context_class(**payload)

        for name, value in kwargs.items():
            setattr(self.context, name, value)

    def _validate(self):
        """
        Performs the validations for the request as per the validators defined in the class attributes
        :return:
        """
        # list of errors consisting of dictionary with error message and error code
        validator_errors = []

        # validating the configuration related validators first, if any error raised in these then no need to validate
        # the payload related validators.
        if not self._execute_validators(self.configuration_validators, validator_errors):
            # validating the payload or data related validators
            self._execute_validators(self.payload_validators, validator_errors)

        # update the errors in the response object
        if validator_errors:
            self.response.success = False
            self.response.errors = validator_errors

    def _execute_validators(self, validators, validator_errors):
        """
        Executes the validator for the list of validators passed all together and appends the errors in the
        validator_errors
        :param validators: List of validators to be executed
        :param validator_errors: List of validation errors raised during overall validation of activity
        :return:
        """
        for Validator in validators:
            try:
                # TODO: make sure context object is referenced so that updates in validators are reflected here
                Validator(self.context, self.user_uuid, self.request_id).validate()
            except ExceptionBase as e:
                validator_errors.append(Error(e.error_code, e.error_message))
        return validator_errors

    @abstractmethod
    def _execute(self):
        """
        This method needs to be implemented in the inherited class only and it will consist of actual
        steps to be performed in the activity.

        And it must also append the data into the response.

        :param payload: Dictionary consisting of payload present in the request directly passed after serialization
        :return:
        """
        raise NotImplementedError('Validate not implemented')

    def _publish_to_topics(self):
        """
        This method will publish the payload to the topics present in the publishing_topic tuple if the activity
        gets completed successfully.

        Note - Retries and fault tolerance will be handled by the published code and not the activity.
        :return:
        """
        for topic in self.publishing_topics:
            #  TODO: publish to topics
            pass
