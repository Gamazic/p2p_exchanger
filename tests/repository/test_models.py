from src.repository.binance_api.models import (AdvertiserSearchApi,
                                               AdvSearchApi, CryptoCurrency,
                                               FiatCurrency, P2POrderSearchApi,
                                               P2PTradeType, SearchApiParams,
                                               SearchApiResponse)

EXAMPLE_RAW_SEARCH_API_PARAMS = {
    "proMerchantAds": False,
    "page": 1,
    "rows": 10,
    "payTypes": [],
    "countries": [],
    "publisherType": "merchant",
    "asset": "USDT",
    "fiat": "RUB",
    "tradeType": "BUY",
}
EXAMPLE_SEARCH_API_PARAMS = SearchApiParams(
    pro_merchant_ads=False,
    page=1,
    rows=10,
    pay_types=[],
    countries=[],
    publisher_type="merchant",
    asset=CryptoCurrency.USDT,
    fiat=FiatCurrency.RUB,
    trade_type=P2PTradeType.BUY,
)


def test_params():
    assert (
        EXAMPLE_SEARCH_API_PARAMS.dict(by_alias=True, exclude_none=True)
        == EXAMPLE_RAW_SEARCH_API_PARAMS
    )


EXAMPLE_SEARCH_API_RESPONSE = {
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
                        "identifier": "Payeer",
                        "iconUrlColor": None,
                        "tradeMethodName": "Payeer",
                        "tradeMethodShortName": "Payeer",
                        "tradeMethodBgColor": "#03A9F4",
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


def test_response():
    parsed_search_api = SearchApiResponse.parse_obj(EXAMPLE_SEARCH_API_RESPONSE)
    search_api_response = SearchApiResponse(
        code="000000",
        data=[
            P2POrderSearchApi(
                adv=AdvSearchApi(
                    maxSingleTransAmount=5001.0,
                    minSingleTransAmount=5000.0,
                    price=61.82,
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
    assert search_api_response == parsed_search_api
