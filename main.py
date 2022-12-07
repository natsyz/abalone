from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import RedirectResponse
import pandas as pd
import base64

from src.abalone.pipelines.data_preprocessing.nodes import drop_dataset, preprocessing
from src.abalone.pipelines.modeling.nodes import preparation, modeling

app = FastAPI()

@app.get('/')
async def docs_redirect():
    """Dokumentasi API"""
    return RedirectResponse(url='/docs')

@app.post("/modeling/")
async def dt_model(
    file: UploadFile = File(...),
    columns: list = Form(None),
    label: str = Form(...),
    max_depth: int = Form(...)
):
    """Modeling dengan model decision tree, kemudian melakukan
    evaluasi dan visualisasi dari decision tree yang dibuat.

    file -- Dataset yang akan dijadikan input modeling
    columns -- List kolom pada dataset yang akan di-drop
    label -- Nama kolom yang merupakan label dari data
    max_depth -- Angka kedalaman decision tree
    """
    raw_df = pd.read_csv(file.file)
    # Data preprocessing
    cleaned_df = preprocessing(drop_dataset(raw_df, columns))
    # Modeling
    data_train, data_test, label_train, label_test = preparation(cleaned_df, label)
    output = modeling(data_train, data_test, label_train, label_test, max_depth)
    # Process output
    lst = [y.strip() for x in output.split("\n") for y in x.split(":")]
    evaluation = dict(zip(lst[::2],list(map(float,lst[1::2]))))
    
    filepath = "data/08_reporting/decession_tree_plot.png"
    with open(filepath, "rb") as image_file:
        encoded_image_string = base64.b64encode(image_file.read())
    
    response = {
        "mime" : "image/png",
        "image": encoded_image_string,
        "evaluation": evaluation
    }

    return response