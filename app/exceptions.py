class AppError(Exception):
    status_code = 500
    code = "internal_error"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ExternalServiceError(AppError):
    status_code = 502
    code = "external_service_error"


class ConfigurationError(AppError):
    status_code = 503
    code = "configuration_error"
