# coding: utf-8

"""
    Skyfire API

    The Skyfire API is designed to allow agents to interact with the Skyfire platform to enable autonomous payments.

    The version of the OpenAPI document: 1.0.0
    Contact: support@skyfire.xyz
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from skyfire_api.models.wallet_balance import WalletBalance

class TestWalletBalance(unittest.TestCase):
    """WalletBalance unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> WalletBalance:
        """Test WalletBalance
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `WalletBalance`
        """
        model = WalletBalance()
        if include_optional:
            return WalletBalance(
                address = '',
                network = '',
                onchain = skyfire_api.models.wallet_balance_onchain.WalletBalance_onchain(
                    total = '', ),
                escrow = skyfire_api.models.wallet_balance_escrow.WalletBalance_escrow(
                    allowance = '', 
                    available = '', 
                    total = '', ),
                claims = skyfire_api.models.wallet_balance_claims.WalletBalance_claims(
                    received = '', 
                    sent = '', ),
                native = skyfire_api.models.wallet_balance_native.WalletBalance_native(
                    balance = '', )
            )
        else:
            return WalletBalance(
                address = '',
                network = '',
                onchain = skyfire_api.models.wallet_balance_onchain.WalletBalance_onchain(
                    total = '', ),
                escrow = skyfire_api.models.wallet_balance_escrow.WalletBalance_escrow(
                    allowance = '', 
                    available = '', 
                    total = '', ),
                claims = skyfire_api.models.wallet_balance_claims.WalletBalance_claims(
                    received = '', 
                    sent = '', ),
                native = skyfire_api.models.wallet_balance_native.WalletBalance_native(
                    balance = '', ),
        )
        """

    def testWalletBalance(self):
        """Test WalletBalance"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
