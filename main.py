import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from handlers import CompensationDataHandler

app = FastAPI()

DATASET_PATH = 'datasets/salary_survey.csv'


@app.get('/compensation_data/')
def get_compensation_data(request: Request):
    result = CompensationDataHandler(DATASET_PATH).handle(request)
    return JSONResponse(jsonable_encoder(result))


@app.get('/compensation_data/columns/')
def get_compensation_data_columns():
    result = list(CompensationDataHandler(DATASET_PATH).dataset_cols)
    return JSONResponse(jsonable_encoder(result))


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
