from typing import Optional, Dict

import uvicorn
from fastapi import FastAPI, Path
from google.cloud import firestore
from pydantic import BaseModel

app = FastAPI()

db = firestore.Client()

debug = True


@app.get("/")
@app.get("/{service_id}")
async def index(*, service_id: int = Path(None, description="The ID of the service you are trying to check"),
                name: Optional[str] = None):
    return {"Hello": f"Service ID {service_id} Service Name: {name}"}


# africastalking callbacks
class ATCallback(BaseModel):
    phoneNumber: str
    description: str
    status: str
    requestId: str
    discount: str
    value: str


@app.post("/at-airtime-callback")
async def at_airtime_callback(at_callback: ATCallback):
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
    return at_callback


# Kyanda callbacks
class KyandaCallback(BaseModel):
    category: str
    source: str
    destination: str
    MerchantID: str
    details: Dict
    status: str
    status_code: str
    message: str
    transactionDate: str
    transactionRef: str
    amount: str


@app.post("/kyanda-callback")
async def kyanda_callback(kyanda_callback: KyandaCallback):
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
        table_name = 'KYANDA_IPN_TRANSACTION'
        if debug:
            table_name += '_TEST'
        kyanda_callback.transactionRef
        doc_ref = db.collection(table_name.lower()).document(kyanda_callback.transactionRef)
        doc = doc_ref.get()
        status = 'Exists'
        if not doc.exists:
            doc_ref.set(dict(kyanda_callback))
            status = 'Success'

        return {"status": status}
    except Exception as ex:
        return {"status": 'Failed'}


# mpesa callbacks
@app.post("/stk-push-callback")
async def stk_push_callback():
    return {"Hello": "World"}


@app.post("/stk-reversal-callback")
async def stk_reversal_callback():
    return {"Hello": "World"}


@app.post("/c2b-callback")
async def c2b_callback():
    return {"Hello": "World"}


@app.post("/transaction-status-callback")
async def c2b_callback():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run('api:app', host="0.0.0.0", port=8000, reload=True)
