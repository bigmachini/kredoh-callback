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
