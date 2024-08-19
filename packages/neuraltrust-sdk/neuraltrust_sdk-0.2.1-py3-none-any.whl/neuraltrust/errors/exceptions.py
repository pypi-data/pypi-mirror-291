from typing import Optional

class NeuralTrustMessages:
    """
    User facing messages.
    """

    SIGN_UP_FOR_BEST_EXPERIENCE = """
For the best experience, sign up at https://neuraltrust.ai and set a NeuralTrust API key.

See https://docs.neuraltrust.ai/evals/quick_start for more information.
"""
    
    NO_NEURALTRUST_API_KEY = """
Please set a NeuralTrust API key.

See https://docs.neuraltrust.ai/evals/quick_start for more info.
    """

    NO_OPENAI_API_KEY = """
Please set an OpenAI API key.

See https://docs.neuraltrust.ai/evals/quick_start for more info.
    """



class CustomException(Exception):
    def __init__(
        self, message: Optional[str] = None, extra_info: Optional[dict] = None
    ):
        self.message = message
        self.extra_info = extra_info
        super().__init__(self.message)

    def __str__(self):
        if self.extra_info:
            return f"{self.message} (Extra Info: {self.extra_info})"
        return self.message


class NoNeuralTrustApiKeyException(CustomException):
    def __init__(self, message: str = NeuralTrustMessages.SIGN_UP_FOR_BEST_EXPERIENCE):
        super().__init__(message)


class NoOpenAiApiKeyException(CustomException):
    def __init__(self, message: str = NeuralTrustMessages.NO_OPENAI_API_KEY):
        super().__init__(message)

class ImportError(CustomException):
    def __init__(self, missing_package: str) -> None:
        super().__init__(message=f"The '{missing_package}' Python package is not installed; please execute 'pip install {missing_package}' to obtain it.")