import streamlit as st
import requests

# Simple Page Title
st.title("💳 Credit Card Fraud Detection System")
st.write("Enter transaction details below to check if the transaction is **Legit** or a **Fraud**.")
st.divider()

# 1. Inputs lene ke liye simple columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Sender Details")
    step = st.number_input("System Step (Time in Hours)", min_value=1, value=1)
    tx_type = st.selectbox("Transaction Type", ["TRANSFER", "CASH_OUT", "PAYMENT", "DEBIT"])
    amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=500.0)
    old_balance_org = st.number_input("Sender Old Balance ($)", min_value=0.0, value=5000.0)
    new_balance_org = st.number_input("Sender New Balance ($)", min_value=0.0, value=4500.0)

with col2:
    st.subheader("🎯 Receiver Details")
    name_orig = st.text_input("Sender Account ID", value="C12345678")
    name_dest = st.text_input("Receiver Account ID", value="M99988877")
    old_balance_dest = st.number_input("Receiver Old Balance ($)", min_value=0.0, value=0.0)
    new_balance_dest = st.number_input("Receiver New Balance ($)", min_value=0.0, value=0.0)

st.divider()

# 2. Prediction Button Logic
if st.button("🔍 Check for Fraud", type="primary", use_container_width=True):
    
    # Payload banana backend ke liye
    payload = {
        "step": int(step),
        "type": tx_type,
        "amount": float(amount),
        "nameOrig": name_orig,
        "oldbalanceOrg": float(old_balance_org),
        "newbalanceOrig": float(new_balance_org),
        "nameDest": name_dest,
        "oldbalanceDest": float(old_balance_dest),
        "newbalanceDest": float(new_balance_dest)
    }
    
    try:
        # FastAPI to hit karna
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        prediction = response.json().get('response', 'Error')
        
        # Result display
        if "Fraud" in prediction:
            st.error(f"### 🚨 ALERT: This transaction is flagged as FRAUD!")
        else:
            st.success(f"### ✅ SUCCESS: This transaction is LEGIT.")
            
    except Exception as e:
        st.error(f"Backend Server running nahi hai bhai! Run uvicorn first. Error: {e}")