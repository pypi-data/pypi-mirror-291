# coding: utf-8

"""
    Skyfire API

    The Skyfire API is designed to allow agents to interact with the Skyfire platform to enable autonomous payments.

    The version of the OpenAPI document: 1.0.0
    Contact: support@skyfire.xyz
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from skyfire_api.models.completion_usage import CompletionUsage
from skyfire_api.models.create_chat_completion_response_choices_inner import CreateChatCompletionResponseChoicesInner
from typing import Optional, Set
from typing_extensions import Self

class CreateChatCompletionResponse(BaseModel):
    """
    Represents a chat completion response returned by model, based on the provided input.
    """ # noqa: E501
    id: StrictStr = Field(description="A unique identifier for the chat completion.")
    choices: List[CreateChatCompletionResponseChoicesInner] = Field(description="A list of chat completion choices. Can be more than one if `n` is greater than 1.")
    created: StrictInt = Field(description="The Unix timestamp (in seconds) of when the chat completion was created.")
    model: StrictStr = Field(description="The model used for the chat completion.")
    service_tier: Optional[StrictStr] = Field(default=None, description="The service tier used for processing the request. This field is only included if the `service_tier` parameter is specified in the request.")
    system_fingerprint: Optional[StrictStr] = Field(default=None, description="This fingerprint represents the backend configuration that the model runs with.  Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made that might impact determinism. ")
    usage: Optional[CompletionUsage] = None
    __properties: ClassVar[List[str]] = ["id", "choices", "created", "model", "service_tier", "system_fingerprint", "usage"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of CreateChatCompletionResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in choices (list)
        _items = []
        if self.choices:
            for _item in self.choices:
                if _item:
                    _items.append(_item.to_dict())
            _dict['choices'] = _items
        # override the default output from pydantic by calling `to_dict()` of usage
        if self.usage:
            _dict['usage'] = self.usage.to_dict()
        # set to None if service_tier (nullable) is None
        # and model_fields_set contains the field
        if self.service_tier is None and "service_tier" in self.model_fields_set:
            _dict['service_tier'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateChatCompletionResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "choices": [CreateChatCompletionResponseChoicesInner.from_dict(_item) for _item in obj["choices"]] if obj.get("choices") is not None else None,
            "created": obj.get("created"),
            "model": obj.get("model"),
            "service_tier": obj.get("service_tier"),
            "system_fingerprint": obj.get("system_fingerprint"),
            "usage": CompletionUsage.from_dict(obj["usage"]) if obj.get("usage") is not None else None
        })
        return _obj


