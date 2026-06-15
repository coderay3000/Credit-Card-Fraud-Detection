from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import predict_output

app=FastAPI()

@app.get('/')
def home():
    return {'message':'Fraud detection API'}

@app.post('/predict')
def predict_premium(data:UserInput):

    user_input={
          'step': data.step,
          'newbalanceOrig': data.newbalanceOrig,
          'newbalanceDest': data.newbalanceDest,
          'dest_is_merchant' : data.dest_is_merchant,
          'errorBalanceOrig' : data.errorBalanceOrig,
          'errorBalanceDest' : data.errorBalanceDest,
          'hour_of_day'  :  data.hour_of_day,
          'day_of_week' :    data.day_of_week,   
          'is_round_amount' : data.is_round_amount,    
          'log_amount'   :  data.log_amount ,
          'type_CASH_OUT' :  data.type_CASH_OUT,     
          'type_DEBIT' :  data.type_DEBIT,       
          'type_PAYMENT': data.type_PAYMENT,       
          'type_TRANSFER' : data.type_TRANSFER
    }

    try:
        prediction=predict_output(user_input)
         
        if prediction==1:
            result_status="Fraud Transaction Detected"
        
        else:
            result_status="Legit (NON_FRAUD) Transaction"

        return JSONResponse(status_code=200,content={'response':result_status})

    except Exception as e:
     
        return JSONResponse(status_code=500,content=str(e))