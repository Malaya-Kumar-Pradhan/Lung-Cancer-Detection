import pandas as pd

def bmi_calc(value):
    if(value<18.5):
        return 0
    elif(value>=18.5 and value<=24.9):
        return 1
    elif(value>=25 and value<=29.9):
        return 2
    elif(value>=30):
        return 3

def cholesterol_calc(value):
    if(value<200):
        return 0
    elif(value>=200 and value<=239):
        return 1
    elif(value>=240):
        return 2

def date_converter(value):
    return pd.to_datetime(value)

def age_speciifer(age):
    if(age<=18):
        return 0
    elif(age>=19 and age<=64):
        return 1
    elif(age>=65):
        return 2
    
def end_treatment(diagnosis_date,end_treatment_date,age):
    a=date_converter(diagnosis_date)
    b=date_converter(end_treatment_date)
    timegap=b.year-a.year
    if(timegap!=0):
        v=age+timegap
    else:
        v=age

    return age_speciifer(v)
