import pickle

ord1= pickle.load(open('ord1.pkl', 'rb'))
ord2= pickle.load(open('ord2.pkl', 'rb'))
ord3= pickle.load(open('ord3.pkl', 'rb'))
ord4= pickle.load(open('ord4.pkl', 'rb'))
ord5= pickle.load(open('ord5.pkl', 'rb'))
ord6= pickle.load(open('ord6.pkl', 'rb'))

def cancer_encoder(value):
    return ord1.transform([[value]])

def smoking_encoder(value):
    return ord2.transform([[value]])

def treatment_encoder(value):
    return ord3.transform([[value]])

def gender_encoder(value):
    return ord4.transform([[value]])

def family_encoder(value):
    return ord5.transform([[value]])

def country_encoder(value):
    return ord6.transform([[value]])