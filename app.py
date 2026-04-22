import streamlit as st
import pandas as pd
import io
import os

DATA_FILE = "persistent_expenses.csv"

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("Persistent Expense Tracker")

# 1. Load Data
if os.path.exists(DATA_FILE):
    st.session_state.expense_data = pd.read_csv(DATA_FILE).to_dict('records')
else:
    if 'expense_data' not in st.session_state:
        st.session_state.expense_data = []

# 2. Input Form
with st.form("expense_form", clear_on_submit=True):
    date = st.date_input("Date")
    categories = ['Food', 'Transport', 'Auto', 'Rapido', 'Bills', 'Railway', 'Other]
    category = st.selectbox("Category", categories)
    amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add to List")

if submitted:
    new_entry = {"Date": str(date), "Category": category, "Amount": amount}
    st.session_state.expense_data.append(new_entry)
    pd.DataFrame(st.session_state.expense_data).to_csv(DATA_FILE, index=False)
    st.success(f"Added entry for {date}!")

# 3. Display, Summary, and Export
if st.session_state.expense_data:
    df = pd.DataFrame(st.session_state.expense_data)
    
    st.divider()
    st.subheader("Spending Summary")
    
    # Select date to view total
    view_date = st.date_input("Select date to see total spending", value=pd.to_datetime(df['Date']).max())
    total_for_date = df[df['Date'] == str(view_date)]['Amount'].sum()
    
    # Currency updated to ₹
    col1, col2 = st.columns(2)
    col1.metric(label=f"Total for {view_date}", value=f"₹{total_for_date:,.2f}")
    col2.metric(label="Grand Total (All Time)", value=f"₹{df['Amount'].sum():,.2f}")
    st.divider()

    st.write("### All Saved Entries", df)

    if st.button("Clear All Data"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.session_state.expense_data = []
        st.rerun()

    # Excel Export
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
