from fastapi import Request, APIRouter
import time

from . import store_to_firestore
from .schemas import kyandaBillTransaction

debug = True
router = APIRouter(
    tags=['Kyanda'],
    prefix='/kyanda'
)

MERCHANT_ID = 'kredoh'
base_url = ''  # app_secret['kyanda_api']['base_url']
API_KEY = ''  # app_secret['kyanda_api']['api_key']


def _get_signature(message):
    import hashlib
    import hmac
    message = bytes(message, 'utf-8')
    secret = bytes(API_KEY, 'utf-8')
    signature = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()
    return signature


# bill transaction
@router.post("/bill-transaction")
async def bill_transaction_api(bill_transaction: kyandaBillTransaction, request: Request):
    """
    This will be called when placing a kyanda bill transaction

    :return: \n
        {
            'status' : 'Success'
        }
    """
    try:
        signature = f'{bill_transaction.amount}{bill_transaction.account}{bill_transaction.telco}{bill_transaction.initiator_phone}{MERCHANT_ID}'
        txn_id = _get_signature(signature + bill_transaction.transaction_id)

        payload = {
            "MerchantID": MERCHANT_ID,
            "account": bill_transaction.account,
            "amount": bill_transaction.amount,
            "telco": bill_transaction.telco,
            "initiatorPhone": bill_transaction.initiator_phone,
            "signature": _get_signature(signature),
            "transaction_id": bill_transaction.transaction_id
        }

        table_name = request.url.path[1:].replace('/', '-')
        result = store_to_firestore(txn_id, payload, request.url.path, table_name)
        return {"status": 'Success' if result else 'Exists'}
    except Exception as ex:
        return {"status": 'Failed'}

#
# # Kyanda callbacks
# @router.post("/kyanda-callback")
# async def kyanda_callback_api(kyanda_callback: KyandaCallback, request: Request):
#     """
#     This callback will be called when transactions are processed via kyanda \n
#     :return:\n
#         { "status" : "Success/Exists/Failed" }
#     *Success* --> record was added to firestore successfully\n
#     *Exists* --> record already exists in firestore\n
#     *Failed* --> Exception occurred
#     """
#     try:
#         result = store_to_firestore(kyanda_callback.transactionRef, kyanda_callback.dict(), request.url.path)
#         return {"status": 'Success' if result else 'Exists'}
#     except Exception as ex:
#         return {"status": 'Failed'}
#
#
# # mpesa callbacks
# @router.post("/stk-push-callback")
# async def stk_push_callback_api(stk_callback: StkPushCallback, request: Request):
#     """
#       This callback will be called when processing of stk_push is done
#       The data is in the format:
#       :return:
#       \n
#           { "status" : "Success/Exists/Failed" }
#       *Success* --> record was added to firestore successfully\n
#       *Exists* --> record already exists in firestore\n
#       *Failed* --> Exception occurred
#       """
#     try:
#         result = store_to_firestore(stk_callback.Body.stkCallback.MerchantRequestID, stk_callback.dict(),
#                                     request.url.path)
#         return {"status": 'Success' if result else 'Exists'}
#     except Exception as ex:
#         return {"status": 'Failed'}
#
#
# @router.post("/c2b-callback")
# async def c2b_callback_api(c2b_callback: C2BCallback, request: Request):
#     """
#          This callback will be called when processing of stk_push is done \n
#
#          :return:
#          \n
#              { "status" : "Success/Exists/Failed" }
#          *Success* --> record was added to firestore successfully\n
#          *Exists* --> record already exists in firestore\n
#          *Failed* --> Exception occurred
#     """
#     try:
#         result = store_to_firestore(c2b_callback.TransID, c2b_callback.dict(),
#                                     request.url.path)
#         return {"status": 'Success' if result else 'Exists'}
#     except Exception as ex:
#         return {"status": 'Failed'}
#
#
# @router.post("/transaction-status-callback")
# async def transactions_status_callback_api(ts_callback: TransactionStatusCallback, request: Request):
#     """
#          This callback will be called when processing of stk_push is done \n
#          :return:
#          \n
#              { "status" : "Success/Exists/Failed" }
#          *Success* --> record was added to firestore successfully\n
#          *Exists* --> record already exists in firestore\n
#          *Failed* --> Exception occurred
#     """
#     try:
#         result = store_to_firestore(ts_callback.Result.ConversationID, ts_callback.dict(),
#                                     request.url.path)
#         return {"status": 'Success' if result else 'Exists'}
#     except Exception as ex:
#         return {"status": 'Failed'}
#
#
# @router.post("/stk-reversal-callback")
# async def mpesa_reversal_callback(reversal_callback: ReversalCallback, request: Request):
#     """
#          This callback will be called when processing of stk_push is done \n
#          :return:
#          \n
#              { "status" : "Success/Exists/Failed" }
#          *Success* --> record was added to firestore successfully\n
#          *Exists* --> record already exists in firestore\n
#          *Failed* --> Exception occurred
#     """
#     try:
#         result = store_to_firestore(reversal_callback.Result.ConversationID, reversal_callback.dict(),
#                                     request.url.path)
#         return {"status": 'Success' if result else 'Exists'}
#     except Exception as ex:
#         return {"status": 'Failed'}
