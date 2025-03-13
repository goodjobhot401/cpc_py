import hmac
import hashlib
import requests
from cpc.common.config import MEXC_HOST
from urllib.parse import urlencode, quote


# ============================================================
# This section of code is extracted from the MEXC API SDK.
# Original GitHub repository: https://github.com/mexcdevelop/mexc-api-sdk
#
# The following is the MIT License text from the original code:
#
# MIT License
#
# Copyright (c) 2021 mxcdevelop
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Note: This is a partial extraction of the original code, with no modifications.
# ============================================================


class TOOL(object):
    def _get_server_time(self):
        return requests.request('get', 'https://api.mexc.com/api/v3/time').json()['serverTime']

    def _sign_v3(self, req_time, sign_params=None):
        if sign_params:
            sign_params = urlencode(sign_params, quote_via=quote)
            to_sign = "{}&timestamp={}".format(sign_params, req_time)
        else:
            to_sign = "timestamp={}".format(req_time)
        sign = hmac.new(self.mexc_secret.encode('utf-8'),
                        to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        return sign

    def public_request(self, method, url, params=None):
        url = '{}{}'.format(self.hosts, url)
        return requests.request(method, url, params=params)

    def sign_request(self, method, url, params=None):
        url = '{}{}'.format(self.hosts, url)
        req_time = self._get_server_time()
        if params:
            params['signature'] = self._sign_v3(
                req_time=req_time, sign_params=params)
        else:
            params = {}
            params['signature'] = self._sign_v3(req_time=req_time)
        params['timestamp'] = req_time
        headers = {
            'x-mexc-apikey': self.mexc_key,
            'Content-Type': 'application/json',
        }
        return requests.request(method, url, params=params, headers=headers)


# Market Data
class mexc_market(TOOL):
    def __init__(self):
        self.api = '/api/v3'
        self.hosts = MEXC_HOST
        self.method = 'GET'

    def get_ping(self):
        """test connectivity"""
        url = '{}{}'.format(self.api, '/ping')
        response = self.public_request(self.method, url)
        return response.json()

    def get_timestamp(self):
        """get sever time"""
        url = '{}{}'.format(self.api, '/time')
        response = self.public_request(self.method, url)
        return response.json()

    def get_defaultSymbols(self):
        """get defaultSymbols"""
        url = '{}{}'.format(self.api, '/defaultSymbols')
        response = self.public_request(self.method, url)
        return response.json()

    def get_exchangeInfo(self, params=None):
        """get exchangeInfo"""
        url = '{}{}'.format(self.api, '/exchangeInfo')
        response = self.public_request(self.method, url, params=params)
        return response.json()

    def get_depth(self, params):
        """get symbol depth"""
        url = '{}{}'.format(self.api, '/depth')
        response = self.public_request(self.method, url, params=params)
        return response.json()

    def get_deals(self, params):
        """get current trade deals list"""
        url = '{}{}'.format(self.api, '/trades')
        response = self.public_request(self.method, url, params=params)
        return response.json()

    def get_aggtrades(self, params):
        """get aggregate trades list"""
        url = '{}{}'.format(self.api, '/aggTrades')
        response = self.public_request(self.method, url, params=params)
        return response.json()

    def get_kline(self, params):
        """get k-line data"""
        url = '{}{}'.format(self.api, '/klines')
        response = self.public_request(self.method, url, params=params)
        return response.json()

    def get_avgprice(self, params):
        """get current average prcie(default : 5m)"""
        url = '{}{}'.format(self.api, '/avgPrice')
        response = self.public_request(self.method, url, params=params)
        return response.json()

    def get_24hr_ticker(self, params=None):
        """get 24hr prcie ticker change statistics"""
        url = '{}{}'.format(self.api, '/ticker/24hr')
        response = self.public_request(self.method, url, params=params)
        return response.json()

    def get_price(self, params=None):
        """get symbol price ticker"""
        url = '{}{}'.format(self.api, '/ticker/price')
        response = self.public_request(self.method, url, params=params)
        return response.json()

    def get_bookticker(self, params=None):
        """get symbol order book ticker"""
        url = '{}{}'.format(self.api, '/ticker/bookTicker')
        response = self.public_request(self.method, url, params=params)
        return response.json()

    def get_ETF_info(self, params=None):
        """get ETF information"""
        url = '{}{}'.format(self.api, '/etf/info')
        response = self.public_request(self.method, url, params=params)
        return response.json()
