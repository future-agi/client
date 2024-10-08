from typing import Optional, Union
from abc import ABC, abstractmethod
from collections.abc import Iterable

from .constants import API_KEY_ENVVAR_NAME, MAX_NUMBER_OF_EMBEDDINGS, SECRET_KEY_ENVVAR_NAME
from .types import ModelTypes, Environments


class ValidationError(Exception, ABC):
    def __str__(self) -> str:
        return self.error_message()

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def error_message(self) -> str:
        pass


class AuthError(Exception):
    def __init__(self, api_key: Optional[str], space_key: Optional[str]) -> None:
        self.missing_api_key = api_key is None
        self.missing_space_key = space_key is None

    def __repr__(self) -> str:
        return "Invalid_TFC_Client_Authentication"

    def __str__(self) -> str:
        return self.error_message()

    def error_message(self) -> str:
        missing_list = ["api_key"] if self.missing_api_key else []
        if self.missing_space_key:
            missing_list.append("space_key")

        return (
            "TFC Client could not obtain credentials. You can pass your api_key and space_key "
            "directly to the TFC Client, or you can set environment variables which will be read if the "
            "keys are not directly passed. "
            "To set the environment variables use the following variable names: \n"
            f" - {API_KEY_ENVVAR_NAME} for the api key\n"
            f" - {SECRET_KEY_ENVVAR_NAME} for the secret key\n"
            f"Missing: {missing_list}"
        )


class InvalidAdditionalHeaders(ValidationError):
    def __repr__(self) -> str:
        return "Invalid_Additional_Headers"

    def __init__(self, invalid_headers: Iterable) -> None:
        self.invalid_header_names = invalid_headers

    def error_message(self) -> str:
        return (
            "Found invalid additional header, cannot use reserved headers named: "
            f"{', '.join(map(str, self.invalid_header_names))}."
        )


class InvalidNumberOfEmbeddings(ValidationError):
    def __repr__(self) -> str:
        return "Invalid_Number_Of_Embeddings"

    def __init__(self, number_of_embeddings: int) -> None:
        self.number_of_embeddings = number_of_embeddings

    def error_message(self) -> str:
        return (
            f"The schema contains {self.number_of_embeddings} different embeddings when a maximum of "
            f"{MAX_NUMBER_OF_EMBEDDINGS} is allowed."
        )


class InvalidValueType(Exception):
    def __init__(
            self,
            value_name: str,
            value: Union[bool, int, float, str],
            correct_type: str,
    ) -> None:
        self.value_name = value_name
        self.value = value
        self.correct_type = correct_type

    def __repr__(self) -> str:
        return "Invalid_Value_Type"

    def __str__(self) -> str:
        return self.error_message()

    def error_message(self) -> str:
        return (
            f"{self.value_name} with value {self.value} is of type {type(self.value).__name__}, "
            f"but expected From {self.correct_type}"
        )


class InvalidSupportedType(Exception):
    def __init__(
            self,
            value_name: str,
            value: Union[ModelTypes, Environments],
            correct_type: str,
    ) -> None:
        self.value_name = value_name
        self.value = value
        self.correct_type = correct_type

    def __repr__(self) -> str:
        return "Invalid_Value_Type"

    def __str__(self) -> str:
        return self.error_message()

    def error_message(self) -> str:
        return (
            f"{self.value_name} with value {self.value} is noy supported as of now, "
            f"supported model types are {self.correct_type}"
        )


class MissingRequiredKey(Exception):
    def __init__(self, field_name, missing_key):
        super().__init__(f"Missing required key '{missing_key}' in {field_name}.")


class InvalidVectorLength(Exception):
    def __init__(self, field_name, length, max_length):
        super().__init__(f"Invalid vector length for {field_name}: maximum length is {max_length}, got {length}.")
