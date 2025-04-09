import streamlit as st
import pandas as pd
import mysql.connector

# --- DB Connection ---
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",    
        password="Anuradha@12345",
        database="sqlpython3"
    )

# --- Query Dictionary ---
queries = {
    "1. All Expenses": "SELECT * FROM expense;",
    "2. Total by Category": "SELECT Category, SUM(Amount) AS Total_Amount FROM expense GROUP BY Category;",
    "3. Total by Payment Mode": "SELECT payment_mode, SUM(Amount) AS Total_Amount FROM expense GROUP BY payment_mode;",
    "4. Total Cashback": "SELECT SUM(Cashback) AS Total_Cashback FROM expense;",
    "5. Top 5 Expensive Categories": "SELECT Category, SUM(Amount) AS Total_Spending FROM expense GROUP BY Category ORDER BY Total_Spending DESC LIMIT 5;",
    "6. Transport by Payment Mode": "SELECT Payment_Mode, SUM(Amount) AS Total_Spent FROM expense WHERE Category = 'transport' GROUP BY Payment_Mode;",
    "7. Transactions with Cashback": "SELECT * FROM expense WHERE Cashback > 0;",
    "8. Monthly Total Spending": "SELECT MONTH(Date) AS Month, SUM(Amount) AS Total_Spending FROM expense GROUP BY MONTH(Date) ORDER BY Month;",
    "9. High Spend Months (Investment, Subscription, Stationary)": "SELECT MONTH(Date) AS Month, Category, SUM(Amount) AS Total_Spending FROM expense WHERE Category IN ('investment', 'subscription', 'stationary') GROUP BY MONTH(Date), Category ORDER BY Total_Spending DESC;",
    "10. Recurring Expenses (Monthly)": "SELECT MONTH(Date) AS Month, Category, COUNT(*) AS Occurrences, SUM(Amount) AS Total_Spending FROM expense WHERE Category IN ('investment', 'subscription', 'fees') GROUP BY MONTH(Date), Category ORDER BY Month, Category;",
    "11. Monthly Cashback": "SELECT MONTH(Date) AS Month, SUM(Cashback) AS Total_Cashback FROM expense GROUP BY MONTH(Date) ORDER BY Month;",
    "12. Monthly Spending Trend": "SELECT YEAR(Date) AS Year, MONTH(Date) AS Month, SUM(Amount) AS Total_Spending FROM expense GROUP BY YEAR(Date), MONTH(Date) ORDER BY Year, Month;",
    "13. Grocery Pattern (Weekdays)": "SELECT DAYNAME(Date) AS Day, SUM(Amount) AS Total_Spending, COUNT(*) AS Transactions FROM expense WHERE Category = 'sports & fitness' GROUP BY Day ORDER BY FIELD(Day, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');",
    "14. Priority Categories": "SELECT Category, SUM(Amount) AS Total_Spending, CASE WHEN Category IN ('investment', 'transport', 'stationary', 'sports & fitness', 'fees') THEN 'High Priority' WHEN Category IN ('subscription') THEN 'Low Priority' ELSE 'Uncategorized' END AS Priority_Level FROM expense GROUP BY Category, Priority_Level ORDER BY Priority_Level DESC, Total_Spending DESC;",
    "15. Highest Contribution Category": "SELECT Category, SUM(Amount) AS Total_Spending, (SUM(Amount) / (SELECT SUM(Amount) FROM expense) * 100) AS Percentage_Contribution FROM expense GROUP BY Category ORDER BY Total_Spending DESC LIMIT 1;",
    "16. Amount > 400": "SELECT * FROM expense WHERE Amount > 400;",
    "17. Amount > 400 with Debit Card": "SELECT * FROM expense WHERE Amount > 400 AND payment_mode = 'debit card';",
    "18. Fees with Debit Card": "SELECT * FROM expense WHERE category = 'fees' AND payment_mode = 'debit card';",
    "19. Category with Cricket Description and Amount > 600": "SELECT category FROM expense WHERE description = 'cricket' GROUP BY category HAVING SUM(Amount) > 600 ORDER BY category DESC;",
    "20. Yearly Spending": "SELECT YEAR(date) AS year, SUM(Amount) AS total_spending FROM expense GROUP BY YEAR(date) ORDER BY year;",
    "21. Total Excluding Cashback": "SELECT SUM(Amount - Cashback) AS total_spent FROM expense;",
    "22. Netflix Subscription Spending": "SELECT SUM(Amount) AS total_netflix FROM expense WHERE description LIKE '%netflix subscription%';",
    "23. Average Daily Spending": "SELECT AVG(daily_total) AS average_daily_spending FROM (SELECT date, SUM(Amount - Cashback) AS daily_total FROM expense GROUP BY date) AS daily_data;",
    "24. Pen and Pencil Spending": "SELECT SUM(Amount - Cashback) AS total_stationary FROM expense WHERE description LIKE '%pen and pencil%';",
    "25. Days Spending > 2000": "SELECT date, SUM(Amount - Cashback) AS total_spent FROM expense GROUP BY date HAVING total_spent > 2000;",
    "26. Transactions per Category": "SELECT category, COUNT(*) AS transaction_count FROM expense GROUP BY Category;"
}

# --- Streamlit UI ---
st.set_page_config(page_title="Expense Dashboard", layout="wide")
st.title("💸 Interactive Expense Dashboard")

# --- Sidebar Selection ---
st.sidebar.header("📊 Explore Queries")
selected_query = st.sidebar.selectbox("Select a Query", list(queries.keys()))

# --- Fetch and Display ---
query = queries[selected_query]
conn = get_connection()
df = pd.read_sql(query, conn)
conn.close()

st.subheader(selected_query)
st.dataframe(df, use_container_width=True)

# --- Optional Chart ---
if "SUM" in query or "COUNT" in query:
    try:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if len(numeric_cols) >= 1 and df.shape[1] > 1:
            st.bar_chart(data=df.set_index(df.columns[0])[numeric_cols[0]])
    except:
        pass

# --- Export Option ---
st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="query_result.csv", mime="text/csv")

