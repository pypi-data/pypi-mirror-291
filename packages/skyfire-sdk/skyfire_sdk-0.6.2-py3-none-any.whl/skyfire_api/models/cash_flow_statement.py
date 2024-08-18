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

from datetime import date
from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class CashFlowStatement(BaseModel):
    """
    CashFlowStatement
    """ # noqa: E501
    ticker: Optional[StrictStr] = Field(default=None, description="The ticker symbol.")
    calendar_date: Optional[date] = Field(default=None, description="The date of the cash flow statement.")
    report_period: Optional[date] = Field(default=None, description="The reporting period of the cash flow statement.")
    period: Optional[StrictStr] = Field(default=None, description="The time period of the cash flow statement.")
    net_cash_flow_from_operations: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The net cash flow from operations of the company.")
    depreciation_and_amortization: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The depreciation and amortization of the company.")
    share_based_compensation: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The share-based compensation of the company.")
    net_cash_flow_from_investing: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The net cash flow from investing of the company.")
    capital_expenditure: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The capital expenditure of the company.")
    business_acquisitions_and_disposals: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The business acquisitions and disposals of the company.")
    investment_acquisitions_and_disposals: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The investment acquisitions and disposals of the company.")
    net_cash_flow_from_financing: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The net cash flow from financing of the company.")
    issuance_or_repayment_of_debt_securities: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The issuance or repayment of debt securities of the company.")
    issuance_or_purchase_of_equity_shares: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The issuance or purchase of equity shares of the company.")
    dividends_and_other_cash_distributions: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The dividends and other cash distributions of the company.")
    change_in_cash_and_equivalents: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The change in cash and equivalents of the company.")
    effect_of_exchange_rate_changes: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The effect of exchange rate changes of the company.")
    __properties: ClassVar[List[str]] = ["ticker", "calendar_date", "report_period", "period", "net_cash_flow_from_operations", "depreciation_and_amortization", "share_based_compensation", "net_cash_flow_from_investing", "capital_expenditure", "business_acquisitions_and_disposals", "investment_acquisitions_and_disposals", "net_cash_flow_from_financing", "issuance_or_repayment_of_debt_securities", "issuance_or_purchase_of_equity_shares", "dividends_and_other_cash_distributions", "change_in_cash_and_equivalents", "effect_of_exchange_rate_changes"]

    @field_validator('period')
    def period_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['quarterly', 'ttm', 'annual']):
            raise ValueError("must be one of enum values ('quarterly', 'ttm', 'annual')")
        return value

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
        """Create an instance of CashFlowStatement from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CashFlowStatement from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "ticker": obj.get("ticker"),
            "calendar_date": obj.get("calendar_date"),
            "report_period": obj.get("report_period"),
            "period": obj.get("period"),
            "net_cash_flow_from_operations": obj.get("net_cash_flow_from_operations"),
            "depreciation_and_amortization": obj.get("depreciation_and_amortization"),
            "share_based_compensation": obj.get("share_based_compensation"),
            "net_cash_flow_from_investing": obj.get("net_cash_flow_from_investing"),
            "capital_expenditure": obj.get("capital_expenditure"),
            "business_acquisitions_and_disposals": obj.get("business_acquisitions_and_disposals"),
            "investment_acquisitions_and_disposals": obj.get("investment_acquisitions_and_disposals"),
            "net_cash_flow_from_financing": obj.get("net_cash_flow_from_financing"),
            "issuance_or_repayment_of_debt_securities": obj.get("issuance_or_repayment_of_debt_securities"),
            "issuance_or_purchase_of_equity_shares": obj.get("issuance_or_purchase_of_equity_shares"),
            "dividends_and_other_cash_distributions": obj.get("dividends_and_other_cash_distributions"),
            "change_in_cash_and_equivalents": obj.get("change_in_cash_and_equivalents"),
            "effect_of_exchange_rate_changes": obj.get("effect_of_exchange_rate_changes")
        })
        return _obj


