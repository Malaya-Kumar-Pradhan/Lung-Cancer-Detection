# Lung Disease Prediction Web Application

This repository contains the source code for a Machine Learning-powered web application that predicts the likelihood of a patient having a specific disease based on their medical history and lifestyle factors. 

The backend is built with **FastAPI** and serves a frontend using **Jinja2** templates. It processes user medical data, performs feature engineering on the fly, and serves predictions using a pre-trained ensemble model (`votingModel.pkl`).

**🌐 Live Deployment:** This application is deployed and hosted live on [HuggingFace](https://huggingface.co/).

---

## 🚀 Features

* **FastAPI Backend:** A fast, modern, and asynchronous Python web framework handling routing and model inference.
* **Machine Learning Integration:** Uses a pre-trained Voting Classifier model to predict the presence of disease (`Has Disease` vs `No Disease`).
* **Robust Feature Engineering:** Automatically calculates derived medical indicators directly from the form inputs, including:
  * `smoking_cancer_factor`
  * `metabollic_risk`
  * `adjusted_survival_index`
* **Data Categorization:** Converts raw continuous inputs (BMI, cholesterol, age, dates) into standard categorical buckets for the ML model using custom helper functions.
* **Categorical Encoding:** Uses pre-fitted Ordinal Encoders to reliably transform categorical text inputs (e.g., country, gender, treatment type) into numerical features.

---

## 🛠️ Tech Stack

* **Backend Framework:** Python 3, FastAPI, Uvicorn
* **Data Processing:** Pandas
* **Machine Learning:** Scikit-Learn (Pickle for model/encoder serialization)
* **Frontend:** HTML/CSS (served via Jinja2Templates & StaticFiles)
* **Deployment:** HuggingFace

---

## 📁 Project Structure

* **`main.py`**: The main entry point of the application. It initializes the FastAPI app, configures the template and static directories, handles the `/` and `/predict` routes, and houses the core data pipeline for model inference.
* **`helper.py`**: Contains data processing utilities to categorize continuous variables (e.g., categorizing BMI into weight classes, Cholesterol into risk levels, and calculating age gaps between diagnosis and treatment).
* **`encoder.py`**: Responsible for loading six distinct pre-trained ordinal encoders (`ord1.pkl` through `ord6.pkl`) and transforming categorical form data into numerical arrays.
* **`templates/`**: Directory containing the `index.html` file (the user interface).
* **`static/`**: Directory for static assets (CSS, JS, images).
* **`*.pkl` files**: Serialized Machine Learning artifacts (The Voting Model and 6 Ordinal Encoders).

---

## ⚙️ Data Pipeline 

When a user submits their data via the `/predict` endpoint, the application performs the following steps:
1. **Type Casting:** Converts form strings to numeric values (`age`, `bmi`, `hypertension`, etc.).
2. **Categorization (`helper.py`):** Bins `bmi`, `cholesterol_level`, and `age` into predefined risk/stage tiers. Calculates `end_treatment_age` based on diagnosis and treatment dates.
3. **Encoding (`encoder.py`):** Transforms categorical inputs into machine-readable numerical formats using the loaded pickle encoders.
4. **Feature Generation:** Calculates the metabolic risk, smoking cancer factor, and adjusted survival index based on mathematical relationships between the inputs.
5. **Inference:** Drops intermediate columns, orders the 14 final features exactly as the model expects, and generates a prediction.

---

## 💻 Local Setup & Installation

If you wish to run this project locally on your machine, follow these steps:

### 1. Prerequisites
Ensure you have Python 3.8+ installed. You will also need Git. 
*(Note: Because this project contains large `.pkl` files, ensure you have Git LFS installed to pull the models correctly).*

### 2. Clone the Repository
```bash
git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
cd your-repo-name
```

### 3. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate 
```

### 4. Install Dependencies
```bash
pip install fastapi uvicorn pandas scikit-learn jinja2 python-multipart
```

### 5. Run the Development Server
Start the Uvicorn server by running main.py directly:
```bash
python main.py
```

Alternatively, run it via uvicorn:
```bash
uvicorn main:app --reload
```

### 6. Access the App
Open your web browser and navigate to: http://localhost:8000
