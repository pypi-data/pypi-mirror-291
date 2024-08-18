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

from skyfire_api.models.api_ninja_crypto_price_response import APINinjaCryptoPriceResponse

class TestAPINinjaCryptoPriceResponse(unittest.TestCase):
    """APINinjaCryptoPriceResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> APINinjaCryptoPriceResponse:
        """Test APINinjaCryptoPriceResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `APINinjaCryptoPriceResponse`
        """
        model = APINinjaCryptoPriceResponse()
        if include_optional:
            return APINinjaCryptoPriceResponse(
                symbol = '',
                price = '',
                timestamp = 1.337
            )
        else:
            return APINinjaCryptoPriceResponse(
                symbol = '',
                price = '',
                timestamp = 1.337,
        )
        """

    def testAPINinjaCryptoPriceResponse(self):
        """Test APINinjaCryptoPriceResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
