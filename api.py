import requests
from typing import Union

from fastapi import FastAPI
import uvicorn
import WiseTestData

#uvicorn src.api:app
#uvicorn.run("api:app", port=5001, log_level="info")
#uvicorn.run

app = FastAPI()


@app.get("/")
def read_root():
    runer = WiseTestData.WiseTestData("api", 30, 'TestData2.xlsx', True, False, False)
    runer.make_data()
    return {"sas"}


#Main REST API:
#http://127.0.0.1:8009/generate/True/rows/11/skipshuffle/False/skippairs/False?excel=TestData.xlsx

@app.get("/generate/{generate}/rows/{rows}/skipshuffle/{skipshuffle}/skippairs/{skippairs}")
def read_item(rows: int, generate:str, skipshuffle:str, skippairs:str, excel: Union[str, None] = None):

    if rows<3: return ("ERROR: Please provide at least 3 rows for data generation")
    try:
        if generate=="False": no_generate="True"
        else:
            no_generate="False"
        runer = WiseTestData.WiseTestData("api", rows, excel, no_generate, skipshuffle, skippairs)
        return_json = runer.make_data()
    except: return {"Error in job execution. Make sure you provide correct data in URL and your Excel file path exists. API spec: http://HOST:port/generate/{True|False}/rows/{#rows_to_generate}/skipshuffle/{True|False}/skippairs/{True|False}"}

    return {"Download data from "+ str(excel) +" All pairs JSON:    "+ str(return_json)}


