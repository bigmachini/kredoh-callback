from typing import Optional

from fastapi import Path, Request, APIRouter

from .schemas import ATCallback, KyandaCallback, StkPushCallback, C2BCallback, \
    TransactionStatusCallback, ReversalCallback

debug = True
router = APIRouter(
    tags=['Callback'],
    prefix='/callback'
)


@router.get("/")
@router.get("/{service_id}")
async def index(*, service_id: int = Path(None, description="The ID of the service you are trying to check"),
                name: Optional[str] = None):
    return {"Hello": f"Service ID {service_id} Service Name: {name}"}


# africastalking callbacks
@router.post("/at-airtime-callback")
async def at_airtime_callback_api(at_callback: ATCallback, request: Request):
    """
    This endpoint is called when airtime is disbursed using AT(Africastalking) channel \n

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
@router.post("/kyanda-callback")
async def kyanda_callback_api(kyanda_callback: KyandaCallback, request: Request):
    """
    This callback will be called when transactions are processed via kyanda \n
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
@router.post("/stk-push-callback")
async def stk_push_callback_api(stk_callback: StkPushCallback, request: Request):
    """
      This callback will be called when processing of stk_push is done
      The data is in the format:
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


@router.post("/c2b-callback")
async def c2b_callback_api(c2b_callback: C2BCallback, request: Request):
    """
         This callback will be called when processing of stk_push is done \n

         :return:
         \n
             { "status" : "Success/Exists/Failed" }
         *Success* --> record was added to firestore successfully\n
         *Exists* --> record already exists in firestore\n
         *Failed* --> Exception occurred
    """
    try:
        result = store_to_firestore(c2b_callback.TransID, c2b_callback.dict(),
                                    request.url.path)
        return {"status": 'Success' if result else 'Exists'}
    except Exception as ex:
        return {"status": 'Failed'}


@router.post("/transaction-status-callback")
async def transactions_status_callback_api(ts_callback: TransactionStatusCallback, request: Request):
    """
         This callback will be called when processing of stk_push is done \n
         :return:
         \n
             { "status" : "Success/Exists/Failed" }
         *Success* --> record was added to firestore successfully\n
         *Exists* --> record already exists in firestore\n
         *Failed* --> Exception occurred
    """
    try:
        result = store_to_firestore(ts_callback.Result.ConversationID, ts_callback.dict(),
                                    request.url.path)
        return {"status": 'Success' if result else 'Exists'}
    except Exception as ex:
        return {"status": 'Failed'}


@router.post("/stk-reversal-callback")
async def mpesa_reversal_callback(reversal_callback: ReversalCallback, request: Request):
    """
         This callback will be called when processing of stk_push is done \n
         :return:
         \n
             { "status" : "Success/Exists/Failed" }
         *Success* --> record was added to firestore successfully\n
         *Exists* --> record already exists in firestore\n
         *Failed* --> Exception occurred
    """
    try:
        result = store_to_firestore(reversal_callback.Result.ConversationID, reversal_callback.dict(),
                                    request.url.path)
        return {"status": 'Success' if result else 'Exists'}
    except Exception as ex:
        return {"status": 'Failed'}
