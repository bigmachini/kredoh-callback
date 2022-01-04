from pydantic import BaseModel
from typing import Optional, List


class NameValue(BaseModel):
    Name: str
    Value: Optional[str] = None


class KeyValue(BaseModel):
    Key: str
    Value: Optional[str] = None


class ReferenceData(BaseModel):
    ReferenceItem: KeyValue


class ResultParameters(BaseModel):
    ResultParameter: List[KeyValue]


class CallbackResult(BaseModel):
    ResultType: int
    ResultCode: int
    ResultDesc: str
    OriginatorConversationID: str
    ConversationID: str
    TransactionID: str
    ResultParameters: ResultParameters
    ReferenceData: ReferenceData


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
class CallbackMetadata(BaseModel):
    Item: List[NameValue]


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


# mpesa transaction_status_callback
class TransactionStatusCallback(BaseModel):
    Result: CallbackResult


# mpesa reversal Callback
class ReversalCallback(BaseModel):
    Result: CallbackResult


# KYANDA
class kyandaBillTransaction(BaseModel):
    amount: str
    account: str
    telco: str
    initiator_phone: str
    transaction_id: str
