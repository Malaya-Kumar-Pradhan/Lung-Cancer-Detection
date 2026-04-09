from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from helper import bmi_calc, cholesterol_calc, age_speciifer, end_treatment
from encoder import cancer_encoder,country_encoder,smoking_encoder,treatment_encoder,gender_encoder,family_encoder
import pickle
import pandas as pd

model=pickle.load(open('votingModel.pkl','rb'))

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get('/',response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("index.html",
                                      {"request":request,"user":"Developer"})

@app.post('/predict')
async def predict(request:Request):
    form_data = await request.form()
    data_dict = {key: val for key, val in form_data.items()}

    input_df = pd.DataFrame([data_dict])

    cols_to_fix = ["age", "bmi", "hypertension", "cholesterol_level", "asthma", "cirrhosis", "other_cancer"]
    input_df[cols_to_fix] = input_df[cols_to_fix].apply(pd.to_numeric)

    input_df["bmi"] = bmi_calc(input_df["bmi"][0])
    input_df["cholesterol_level"] = cholesterol_calc(input_df["cholesterol_level"][0])
    input_df["cancer_stage"] = cancer_encoder(input_df["cancer_stage"][0])
    input_df["smoking_status"] = smoking_encoder(input_df["smoking_status"][0])
    input_df["treatment_type"] = treatment_encoder(input_df["treatment_type"][0])
    input_df["gender"] = gender_encoder(input_df["gender"][0])
    input_df["family_history"] = family_encoder(input_df["family_history"][0])
    input_df["country"] = country_encoder(input_df["country"][0])
    input_df["end_treatment_date"] = end_treatment(input_df["diagnosis_date"][0],input_df["end_treatment_date"][0],input_df["age"][0])
    input_df["age"] = age_speciifer(input_df["age"][0])

    input_df["smoking_cancer_factor"] = input_df["cancer_stage"][0] + (input_df["smoking_status"][0] * 0.5)
    input_df["metabollic_risk"] = (input_df["cholesterol_level"][0] * input_df["bmi"][0]) / (input_df["cancer_stage"][0]+1)
    input_df["adjusted_survival_index"] = 1/(input_df["cancer_stage"][0]+input_df["smoking_status"][0]+input_df["cholesterol_level"][0]+1)

    input_df=input_df.rename(columns={
        "age":"diagnosis_age",
        "end_treatment_date":"end_treatment_age"
    })

    del input_df["cancer_stage"]
    del input_df["cholesterol_level"]
    del input_df["smoking_status"]

    train_col = ['gender', 'country', 'family_history', 'bmi', 'hypertension', 'asthma',
       'cirrhosis', 'other_cancer', 'treatment_type', 'end_treatment_age',
       'diagnosis_age', 'smoking_cancer_factor', 'metabollic_risk',
       'adjusted_survival_index']
    final_features = input_df[train_col].values
    prediction = model.predict(final_features)
    output = "Has Disease" if prediction[0]==1 else 'No Disease'
    return templates.TemplateResponse(name='index.html',
                                      context={
                                        "request": request,
                                        "prediction_text": f"Prediction: {output}"
                                    })


if __name__=="__main__":
    import uvicorn
    print("Starting FastAPI Server")
    uvicorn.run(app, host="0.0.0.0", port=8000)