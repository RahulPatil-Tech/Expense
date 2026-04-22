import streamlit as st
import pandas as pd
import io
import os

# File to store data permanently
DATA_FILE = "persistent_expenses.csv"

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("📊 Persistent Expense Tracker")

# 1. Load existing data from CSV if it exists
if os.path.exists(DATA_FILE):
    st.session_state.expense_data = pd.read_csv(DATA_FILE).to_dict('records')
else:
    if 'expense_data' not in st.session_state:
        st.session_state.expense_data = []

# 2. Input Form
with st.form("expense_form", clear_on_submit=True):
    date = st.date_input("Date")
    categories = ['Food', 'Transport', 'Rent', 'Entertainment', 'Bills', 'Other']
    category = st.selectbox("Category", categories)
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add to List")

if submitted:
    new_entry = {"Date": str(date), "Category": category, "Amount": amount}
    st.session_state.expense_data.append(new_entry)
    
    # Save to CSV immediately so it survives a refresh
    pd.DataFrame(st.session_state.expense_data).to_csv(DATA_FILE, index=False)
    st.success("Saved to local storage!")

# 3. Display and Export
if st.session_state.expense_data:
    df = pd.DataFrame(st.session_state.expense_data)
    st.write("### All Saved Entries", df)

    # Clear Data Button
    if st.button("Clear All Data"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.session_state.expense_data = []
        st.rerun()

    # Excel Export with Dropdown
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
          df.to_excel(writer, index=False, sheet_name='Expenses')
          workbook = writer.book
          worksheet = writer.sheets['Expenses']
          worksheet.data_validation('B2:B100', {'validate': 'list', 'source': categories})
    
    st.download_button(
        label="Download Excel File",
        data=output.getvalue(),
        file_name="expenses.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


tput = io.BytesIO()
  
