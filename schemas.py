from pydantic import BaseModel
from typing import Optional, List


# Africastalking Schemas
class ATCallback(BaseModel):
    phoneNumber: str
    description: str
    status: str
    requestId: str
    discount: str
    value: str


# Kyanda Schemas
class KyandaCallbackDetails(BaseModel):
    biller_Receipt: Optional[str] = None
    tokens: Optional[str] = None
    units: Optional[str] = None


class KyandaCallback(BaseModel):
    category: str
    source: str
    destination: str
    MerchantID: str
    details: KyandaCallbackDetails
    status: str
    status_code: str
    message: str
    transactionDate: str
    transactionRef: str
    amount: str


# mpesa stk callback
class CallbackMetadataItem(BaseModel):
    Name: str
    Value: Optional[str] = None


class CallbackMetadata(BaseModel):
    Item: List[CallbackMetadataItem]


class StkCallback(BaseModel):
    MerchantRequestID: str
    CheckoutRequestID: str
    ResultCode: int
    ResultDesc: str
    CallbackMetadata: CallbackMetadata


class StkPushCallbackBody(BaseModel):
    stkCallback: StkCallback


class StkPushCallback(BaseModel):
    Body: StkPushCallbackBody


# mpesa c2b callback
x = {'TransactionType': 'Customer Merchant Payment', 'TransID': 'PLU8V56Y5C', 'TransTime': '20211230104939',
     'TransAmount': '98.00', 'BusinessShortCode': '7195415', 'BillRefNumber': '', 'InvoiceNumber': '',
     'OrgAccountBalance': '11952.81', 'ThirdPartyTransID': '', 'MSISDN': '254708720306', 'FirstName': 'kenneth',
     'MiddleName': 'kihanya', 'LastName': 'waweru'}


class C2BCallback(BaseModel):
    TransactionType: str
    TransID: str
    TransTime: str
    TransAmount: str
    BusinessShortCode: str
    BillRefNumber: str
    InvoiceNumber: str
    OrgAccountBalance: str
    ThirdPartyTransID: str
    MSISDN: str
    FirstName: str
    MiddleName: str
    LastName: str
