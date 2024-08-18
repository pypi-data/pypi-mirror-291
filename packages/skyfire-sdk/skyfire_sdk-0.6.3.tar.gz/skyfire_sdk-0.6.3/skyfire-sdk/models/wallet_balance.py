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

from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List
from skyfire-sdk.models.wallet_balance_claims import WalletBalanceClaims
from skyfire-sdk.models.wallet_balance_escrow import WalletBalanceEscrow
from skyfire-sdk.models.wallet_balance_native import WalletBalanceNative
from skyfire-sdk.models.wallet_balance_onchain import WalletBalanceOnchain
from typing import Optional, Set
from typing_extensions import Self

class WalletBalance(BaseModel):
    """
    WalletBalance
    """ # noqa: E501
    address: StrictStr
    network: StrictStr
    onchain: WalletBalanceOnchain
    escrow: WalletBalanceEscrow
    claims: WalletBalanceClaims
    native: WalletBalanceNative
    __properties: ClassVar[List[str]] = ["address", "network", "onchain", "escrow", "claims", "native"]

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
        """Create an instance of WalletBalance from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of onchain
        if self.onchain:
            _dict['onchain'] = self.onchain.to_dict()
        # override the default output from pydantic by calling `to_dict()` of escrow
        if self.escrow:
            _dict['escrow'] = self.escrow.to_dict()
        # override the default output from pydantic by calling `to_dict()` of claims
        if self.claims:
            _dict['claims'] = self.claims.to_dict()
        # override the default output from pydantic by calling `to_dict()` of native
        if self.native:
            _dict['native'] = self.native.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of WalletBalance from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "address": obj.get("address"),
            "network": obj.get("network"),
            "onchain": WalletBalanceOnchain.from_dict(obj["onchain"]) if obj.get("onchain") is not None else None,
            "escrow": WalletBalanceEscrow.from_dict(obj["escrow"]) if obj.get("escrow") is not None else None,
            "claims": WalletBalanceClaims.from_dict(obj["claims"]) if obj.get("claims") is not None else None,
            "native": WalletBalanceNative.from_dict(obj["native"]) if obj.get("native") is not None else None
        })
        return _obj


