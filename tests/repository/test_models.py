from copy import deepcopy

import pytest
from fastapi.encoders import jsonable_encoder
from src.repository.binance_api.models import (
    AdvertiserSearchApi,
    AdvSearchApi,
    CryptoCurrency,
    FiatCurrency,
    P2POrderSearchApi,
    P2PTradeType,
    RubPayment,
    SearchApiParams,
    SearchApiResponse,
    TradeMethod,
)

EXAMPLE_RAW_SEARCH_API_PARAMS = {
    "page": 1,
    "rows": 10,
    "payTypes": ["TinkoffNew"],
    "countries": [],
    "asset": "USDT",
    "fiat": "RUB",
    "tradeType": "BUY",
    "transAmount": 0,
}
EXAMPLE_2_RAW_SEARCH_API_PARAMS = EXAMPLE_RAW_SEARCH_API_PARAMS | {"asset": "BTC"}
EXAMPLE_SEARCH_API_ARG = SearchApiParams(
    pro_merchant_ads=None,
    page=1,
    rows=10,
    pay_types=frozenset({RubPayment.TinkoffNew}),
    countries=frozenset(),
    publisher_type=None,
    asset=CryptoCurrency.USDT,
    fiat=FiatCurrency.RUB,
    trade_type=P2PTradeType.BUY,
    trans_amount=0.0,
)
EXAMPLE_2_SEARCH_API_ARG = SearchApiParams(**EXAMPLE_SEARCH_API_ARG.dict(exclude={"asset"}), asset=CryptoCurrency.BTC)


class TestSearchApiParams:
    @pytest.mark.parametrize(
        "arg,params",
        [
            (EXAMPLE_SEARCH_API_ARG, EXAMPLE_RAW_SEARCH_API_PARAMS),
            (EXAMPLE_2_SEARCH_API_ARG, EXAMPLE_2_RAW_SEARCH_API_PARAMS),
        ],
    )
    def test_params(self, arg, params):
        assert jsonable_encoder(arg, by_alias=True, exclude_none=True) == params


EXAMPLE_RAW_SEARCH_API_RESPONSE = {
    "code": "000000",
    "message": None,
    "messageDetail": None,
    "data": [
        {
            "adv": {
                "advNo": "11416653472193486848",
                "classify": "mass",
                "tradeType": "SELL",
                "asset": "USDT",
                "fiatUnit": "RUB",
                "advStatus": None,
                "priceType": None,
                "priceFloatingRatio": None,
                "rateFloatingRatio": None,
                "currencyRate": None,
                "price": "61.82",
                "initAmount": None,
                "surplusAmount": "395.97",
                "amountAfterEditing": None,
                "maxSingleTransAmount": "5001.00",
                "minSingleTransAmount": "5000.00",
                "buyerKycLimit": None,
                "buyerRegDaysLimit": None,
                "buyerBtcPositionLimit": None,
                "remarks": None,
                "autoReplyMsg": "",
                "payTimeLimit": None,
                "tradeMethods": [
                    {
                        "payId": None,
                        "payMethodId": "",
                        "payType": None,
                        "payAccount": None,
                        "payBank": None,
                        "paySubBank": None,
                        "identifier": "TinkoffNew",
                        "iconUrlColor": None,
                        "tradeMethodName": "Tинькoфф",
                        "tradeMethodShortName": "Tинькoфф",
                        "tradeMethodBgColor": "#DAB700",
                    }
                ],
                "userTradeCountFilterTime": None,
                "userBuyTradeCountMin": None,
                "userBuyTradeCountMax": None,
                "userSellTradeCountMin": None,
                "userSellTradeCountMax": None,
                "userAllTradeCountMin": None,
                "userAllTradeCountMax": None,
                "userTradeCompleteRateFilterTime": None,
                "userTradeCompleteCountMin": None,
                "userTradeCompleteRateMin": None,
                "userTradeVolumeFilterTime": None,
                "userTradeType": None,
                "userTradeVolumeMin": None,
                "userTradeVolumeMax": None,
                "userTradeVolumeAsset": None,
                "createTime": None,
                "advUpdateTime": None,
                "fiatVo": None,
                "assetVo": None,
                "advVisibleRet": None,
                "assetLogo": None,
                "assetScale": 2,
                "fiatScale": 2,
                "priceScale": 2,
                "fiatSymbol": "₽",
                "isTradable": True,
                "dynamicMaxSingleTransAmount": "5001.00",
                "minSingleTransQuantity": "80.87",
                "maxSingleTransQuantity": "80.89",
                "dynamicMaxSingleTransQuantity": "80.89",
                "tradableQuantity": "395.57",
                "commissionRate": "0.00100000",
                "tradeMethodCommissionRates": [],
                "launchCountry": None,
                "abnormalStatusList": None,
                "closeReason": None,
            },
            "advertiser": {
                "userNo": "s987ef83f7c373b2d939960f36abde794",
                "realName": None,
                "nickName": "Kripto-Monah",
                "margin": None,
                "marginUnit": None,
                "orderCount": None,
                "monthOrderCount": 210,
                "monthFinishRate": 0.996,
                "advConfirmTime": None,
                "email": None,
                "registrationTime": None,
                "mobile": None,
                "userType": "user",
                "tagIconUrls": [],
                "userGrade": 2,
                "userIdentity": "",
                "proMerchant": None,
                "isBlocked": None,
            },
        }
    ],
    "total": 504,
    "success": True,
}
EXAMPLE_RAW_SEARCH_API_RESPONSE_2 = deepcopy(EXAMPLE_RAW_SEARCH_API_RESPONSE)
EXAMPLE_RAW_SEARCH_API_RESPONSE_2["data"][0]["adv"]["price"] = 63
EXAMPLE_2_RAW_SEARCH_API_RESPONSE = deepcopy(EXAMPLE_RAW_SEARCH_API_RESPONSE)
EXAMPLE_2_RAW_SEARCH_API_RESPONSE["data"][0]["adv"]["price"] = 228
EXAMPLE_2_RAW_SEARCH_API_RESPONSE_2 = deepcopy(EXAMPLE_RAW_SEARCH_API_RESPONSE)
EXAMPLE_2_RAW_SEARCH_API_RESPONSE_2["data"][0]["adv"]["price"] = 322
EXAMPLE_RAW_SEARCH_API_RESPONSE_UNSEEN_PAYMENT = {
    "code": "000000",
    "message": None,
    "messageDetail": None,
    "data": [
        {
            "adv": {
                "advNo": "11416653472193486848",
                "classify": "mass",
                "tradeType": "SELL",
                "asset": "USDT",
                "fiatUnit": "RUB",
                "advStatus": None,
                "priceType": None,
                "priceFloatingRatio": None,
                "rateFloatingRatio": None,
                "currencyRate": None,
                "price": "61.82",
                "initAmount": None,
                "surplusAmount": "395.97",
                "amountAfterEditing": None,
                "maxSingleTransAmount": "5001.00",
                "minSingleTransAmount": "5000.00",
                "buyerKycLimit": None,
                "buyerRegDaysLimit": None,
                "buyerBtcPositionLimit": None,
                "remarks": None,
                "autoReplyMsg": "",
                "payTimeLimit": None,
                "tradeMethods": [
                    {
                        "payId": None,
                        "payMethodId": "",
                        "payType": None,
                        "payAccount": None,
                        "payBank": None,
                        "paySubBank": None,
                        "identifier": "IDK",
                        "iconUrlColor": None,
                        "tradeMethodName": "Tинькoфф",
                        "tradeMethodShortName": "Tинькoфф",
                        "tradeMethodBgColor": "#DAB700",
                    }
                ],
                "userTradeCountFilterTime": None,
                "userBuyTradeCountMin": None,
                "userBuyTradeCountMax": None,
                "userSellTradeCountMin": None,
                "userSellTradeCountMax": None,
                "userAllTradeCountMin": None,
                "userAllTradeCountMax": None,
                "userTradeCompleteRateFilterTime": None,
                "userTradeCompleteCountMin": None,
                "userTradeCompleteRateMin": None,
                "userTradeVolumeFilterTime": None,
                "userTradeType": None,
                "userTradeVolumeMin": None,
                "userTradeVolumeMax": None,
                "userTradeVolumeAsset": None,
                "createTime": None,
                "advUpdateTime": None,
                "fiatVo": None,
                "assetVo": None,
                "advVisibleRet": None,
                "assetLogo": None,
                "assetScale": 2,
                "fiatScale": 2,
                "priceScale": 2,
                "fiatSymbol": "₽",
                "isTradable": True,
                "dynamicMaxSingleTransAmount": "5001.00",
                "minSingleTransQuantity": "80.87",
                "maxSingleTransQuantity": "80.89",
                "dynamicMaxSingleTransQuantity": "80.89",
                "tradableQuantity": "395.57",
                "commissionRate": "0.00100000",
                "tradeMethodCommissionRates": [],
                "launchCountry": None,
                "abnormalStatusList": None,
                "closeReason": None,
            },
            "advertiser": {
                "userNo": "s987ef83f7c373b2d939960f36abde794",
                "realName": None,
                "nickName": "Kripto-Monah",
                "margin": None,
                "marginUnit": None,
                "orderCount": None,
                "monthOrderCount": 210,
                "monthFinishRate": 0.996,
                "advConfirmTime": None,
                "email": None,
                "registrationTime": None,
                "mobile": None,
                "userType": "user",
                "tagIconUrls": [],
                "userGrade": 2,
                "userIdentity": "",
                "proMerchant": None,
                "isBlocked": None,
            },
        }
    ],
    "total": 504,
    "success": True,
}
EXAMPLE_SEARCH_API_RETURN = SearchApiResponse(
    code="000000",
    data=[
        P2POrderSearchApi(
            adv=AdvSearchApi(
                max_single_trans_amount=5001.0,
                min_single_trans_amount=5000.0,
                price=61.82,
                trade_methods=[TradeMethod(identifier=RubPayment.TinkoffNew)],
            ),
            advertiser=AdvertiserSearchApi(
                nick_name="Kripto-Monah",
                month_finish_rate=0.996,
                month_order_count=210,
                user_grade=2,
                user_type="user",
                user_identity="",
            ),
        )
    ],
    success=True,
    total=504,
)
EXAMPLE_SEARCH_API_RETURN_2 = deepcopy(EXAMPLE_SEARCH_API_RETURN)
EXAMPLE_SEARCH_API_RETURN_2.data[0].adv.price = 63
EXAMPLE_2_SEARCH_API_RETURN = deepcopy(EXAMPLE_SEARCH_API_RETURN)
EXAMPLE_2_SEARCH_API_RETURN.data[0].adv.price = 228
EXAMPLE_2_SEARCH_API_RETURN_2 = deepcopy(EXAMPLE_SEARCH_API_RETURN)
EXAMPLE_2_SEARCH_API_RETURN_2.data[0].adv.price = 322


class TestSearchApiResponse:
    @pytest.mark.parametrize(
        "expected,parsed",
        [
            (EXAMPLE_SEARCH_API_RETURN, EXAMPLE_RAW_SEARCH_API_RESPONSE),
            (EXAMPLE_SEARCH_API_RETURN_2, EXAMPLE_SEARCH_API_RETURN_2),
            (EXAMPLE_2_SEARCH_API_RETURN, EXAMPLE_2_RAW_SEARCH_API_RESPONSE),
            (EXAMPLE_2_SEARCH_API_RETURN_2, EXAMPLE_2_RAW_SEARCH_API_RESPONSE_2),
        ],
    )
    def test_response(self, expected, parsed):
        parsed_search_api = SearchApiResponse.parse_obj(parsed)
        assert expected == parsed_search_api

    def test_unseen_payment(self):
        SearchApiResponse.parse_obj(EXAMPLE_RAW_SEARCH_API_RESPONSE_UNSEEN_PAYMENT)
