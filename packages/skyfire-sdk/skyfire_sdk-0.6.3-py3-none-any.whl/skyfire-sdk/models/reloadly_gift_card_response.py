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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from skyfire-sdk.models.reloadly_gift_card_response_product import ReloadlyGiftCardResponseProduct
from typing import Optional, Set
from typing_extensions import Self

class ReloadlyGiftCardResponse(BaseModel):
    """
    ReloadlyGiftCardResponse
    """ # noqa: E501
    transaction_id: StrictStr = Field(alias="transactionId")
    amount: Union[StrictFloat, StrictInt]
    discount: Union[StrictFloat, StrictInt]
    currency_code: StrictStr = Field(alias="currencyCode")
    fee: Union[StrictFloat, StrictInt]
    sms_fee: Union[StrictFloat, StrictInt] = Field(alias="smsFee")
    total_fee: Union[StrictFloat, StrictInt] = Field(alias="totalFee")
    pre_ordered: StrictBool = Field(alias="preOrdered")
    recipient_email: StrictStr = Field(alias="recipientEmail")
    recipient_phone: Optional[StrictStr] = Field(default=None, alias="recipientPhone")
    customer_identifier: StrictStr = Field(alias="customerIdentifier")
    status: StrictStr
    transaction_created_time: StrictStr = Field(alias="transactionCreatedTime")
    product: ReloadlyGiftCardResponseProduct
    __properties: ClassVar[List[str]] = ["transactionId", "amount", "discount", "currencyCode", "fee", "smsFee", "totalFee", "preOrdered", "recipientEmail", "recipientPhone", "customerIdentifier", "status", "transactionCreatedTime", "product"]

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
        """Create an instance of ReloadlyGiftCardResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of product
        if self.product:
            _dict['product'] = self.product.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ReloadlyGiftCardResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "transactionId": obj.get("transactionId"),
            "amount": obj.get("amount"),
            "discount": obj.get("discount"),
            "currencyCode": obj.get("currencyCode"),
            "fee": obj.get("fee"),
            "smsFee": obj.get("smsFee"),
            "totalFee": obj.get("totalFee"),
            "preOrdered": obj.get("preOrdered"),
            "recipientEmail": obj.get("recipientEmail"),
            "recipientPhone": obj.get("recipientPhone"),
            "customerIdentifier": obj.get("customerIdentifier"),
            "status": obj.get("status"),
            "transactionCreatedTime": obj.get("transactionCreatedTime"),
            "product": ReloadlyGiftCardResponseProduct.from_dict(obj["product"]) if obj.get("product") is not None else None
        })
        return _obj


