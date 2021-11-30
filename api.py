import uvicorn
from fastapi import FastAPI, Path
from typing import NamedTuple, Optional
from pydantic import BaseModel

app = FastAPI()


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
@app.post("/kyanda-callback")
async def kyanda_callback():
    return {"Hello": "World"}


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
