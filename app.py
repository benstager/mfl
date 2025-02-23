import streamlit as st
import pickle
import numpy as np
import os

current_dir = os.path.dirname('app.py')
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

model_path = os.path.join(parent_dir, "models", "SVM_model_2.pkl")
cols_path = os.path.join(parent_dir, "models", "SVM_model_2_cols.pkl")
scaler_path = os.path.join(parent_dir, "models", "scaler.pkl")

with open('/Users/benstager/Desktop/first round qb model/models/SVM_model_final.pkl', "rb") as f:
    model = pickle.load(f)

with open('/Users/benstager/Desktop/first round qb model/models/scaler_production.pkl', "rb") as f:
    scaler = pickle.load(f)

cols = ['G', 'TD', 'pick', 'Int', 'power_5']

st.title('NFL Model')

st.header('Enter input features:')

feature1 = st.number_input("Enter games played", value=0.0)
feature2 = st.number_input("Enter touchdowns thrown", value=0.0)
feature3 = st.number_input("Enter pick of 1st round", value=0.0)
feature4 = st.number_input("Enter number of interceptions", value=0.0)
feature5 = st.number_input("Enter whether or not they played power 5", value=0.0)

scaled_data = scaler.transform(np.array([[feature1, feature2, feature3, feature4,feature5]]).reshape(1,-1))

if st.button("Predict:"):
    prediction = model.predict(np.array(scaled_data).reshape(1,-1))
    st.success(f'The model predicts {prediction}')