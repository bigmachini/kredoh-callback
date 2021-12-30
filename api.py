from typing import Optional, Dict

import uvicorn
from fastapi import FastAPI, Path, Request
from google.cloud import firestore

from kredoh.callbacks.schemas import ATCallback, KyandaCallback, StkPushCallback, C2BCallback

app = FastAPI()

debug = True


def store_to_firestore(ref: str, data: Dict, path: str):
    table_name = 'CALLBACKS'
    if debug:
        table_name += '_TEST'
    db = firestore.Client()
    doc_ref = db.collection(table_name.lower()).document(ref)
    doc = doc_ref.get()
    if not doc.exists:
        content = {'path': path,
                   'data': data,
                   'ref': ref}
        doc_ref.set(content)
        return True

    return False


@app.get("/")
@app.get("/{service_id}")
async def index(*, service_id: int = Path(None, description="The ID of the service you are trying to check"),
                name: Optional[str] = None):
    return {"Hello": f"Service ID {service_id} Service Name: {name}"}


# africastalking callbacks
@app.post("/at-airtime-callback")
async def at_airtime_callback(at_callback: ATCallback, request: Request):
    """
    This endpoint is called when airtime is disbursed using AT(Africastalking) channel
    The data comes in this format:\n
        {
            "phoneNumber":"+254711XXXYYY",
            "description":"Airtime Delivered Successfully",
            "status":"Success",
            "requestId":"ATQid_SampleTxnId123",
            "discount":"KES 0.6000",
            "value":"KES 100.0000"
        }
    :return: \n
        {
            'status' : 'Success'
        }
    """
    try:
        result = store_to_firestore(at_callback.requestId, at_callback.dict(), request.url.path)
        return {"status": 'Success' if result else 'Exists'}
    except Exception as ex:
        return {"status": 'Failed'}


# Kyanda callbacks
@app.post("/kyanda-callback")
async def kyanda_callback(kyanda_callback: KyandaCallback, request: Request):
    """
    This callback will be called when transactions are processed via kyanda
    The data is in the format:\n
        {
            "category": "UtilityPayment",
            "source": "PaymentWallet",
            "destination": "0715330000",
            "MerchantID": "kyanda",
            "details": { biller_receiptNo: 0105781244210},
            "status": "Success",
            "status_code":"0000",
            "message":"Your Request has been processed successfully.",
            "transactionDate": "20210401091002",
            "transactionRef": "KYAAPI_______",
            "amount": "1500"
        }
    :return:\n
        { "status" : "Success/Exists/Failed" }
    *Success* --> record was added to firestore successfully\n
    *Exists* --> record already exists in firestore\n
    *Failed* --> Exception occurred
    """
    try:
        result = store_to_firestore(kyanda_callback.transactionRef, kyanda_callback.dict(), request.url.path)
        return {"status": 'Success' if result else 'Exists'}
    except Exception as ex:
        return {"status": 'Failed'}


# mpesa callbacks
@app.post("/stk-push-callback")
async def stk_push_callback(stk_callback: StkPushCallback, request: Request):
    """
      This callback will be called when processing of stk_push is done
      The data is in the format:
      \n
          {"Body":
            {"stkCallback":
                {"MerchantRequestID": "837-18118467-1",
                "CheckoutRequestID": "ws_CO_30122021115014387894",
                "ResultCode": 0,
                "ResultDesc": "The service request is processed successfully.",
                "CallbackMetadata": {"Item": [  {"Name": "Amount", "Value": 98},
                                                {"Name": "MpesaReceiptNumber", "Value": "PLU4V8VK6Y"},
                                                {"Name": "Balance"},
                                                {"Name": "TransactionDate", "Value": 20211230115026},
                                                {"Name": "PhoneNumber", "Value": 254721577602}]}}}}
      \n
      :return:
      \n
          { "status" : "Success/Exists/Failed" }
      *Success* --> record was added to firestore successfully\n
      *Exists* --> record already exists in firestore\n
      *Failed* --> Exception occurred
      """
    try:
        result = store_to_firestore(stk_callback.Body.stkCallback.MerchantRequestID, stk_callback.dict(),
                                    request.url.path)
        return {"status": 'Success' if result else 'Exists'}
    except Exception as ex:
        return {"status": 'Failed'}


@app.post("/c2b-callback")
async def c2b_callback(c2b__callback: C2BCallback, request: Request):
    """
         This callback will be called when processing of stk_push is done
         The data is in the format:
         \n
             {
                "TransactionType": "Customer Merchant Payment",
                "TransID": "PLU8V00V00",
                "TransTime": "20211230100000",
                "TransAmount": "98.00",
                "BusinessShortCode": "00000000",
                "BillRefNumber": "",
                "InvoiceNumber": "",
                "OrgAccountBalance": "1000.00",
                "ThirdPartyTransID": "",
                "MSISDN": "254700000000",
                "FirstName": "kenneth",
                "MiddleName": "kihanya",
                "LastName": "waweru"}
         \n
         :return:
         \n
             { "status" : "Success/Exists/Failed" }
         *Success* --> record was added to firestore successfully\n
         *Exists* --> record already exists in firestore\n
         *Failed* --> Exception occurred
    """
    try:
        result = store_to_firestore(c2b__callback.TransID, c2b__callback.dict(),
                                    request.url.path)
        return {"status": 'Success' if result else 'Exists'}
    except Exception as ex:
        return {"status": 'Failed'}


@app.post("/stk-reversal-callback")
async def stk_reversal_callback():
    return {"Hello": "World"}


@app.post("/transaction-status-callback")
async def c2b_callback():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run('api:app', host="0.0.0.0", port=8000, reload=True)
