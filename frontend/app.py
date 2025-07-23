import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- PAGE SETTINGS ---
st.set_page_config(page_title="🤖 GenAI E-commerce Assistant", layout="wide")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .big-title { font-size:30px; font-weight:bold; margin-bottom:10px; }
    .subtle { color:gray; font-size:16px; }
    .gemini-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: 500;
        color: #333;
        margin-top: 10px;
    }
    .dark .gemini-box {
        background-color: #2b2b2b;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="big-title">🧠 GenAI E-commerce Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtle">Ask any business question and get insights powered by Gemini AI</div>', unsafe_allow_html=True)

# --- EXAMPLES ---
with st.expander("💡 Example Questions"):
    st.markdown("""
    - 💰 *What is my total sales?*
    - 🎯 *Which product had the highest CPC?*
    - 🚚 *How many customers are eligible for free delivery?*
    - 📉 *What is my RoAS (Return on Ad Spend)?*
    """)

API_URL = "http://127.0.0.1:5000/api/ask"
st.markdown("---")

# --- INPUT BOX ---
question = st.text_input("💬 Ask your e-commerce data question here:", placeholder="e.g. Show average CPC by product...")

# --- SUBMIT BUTTON ---
if st.button("🚀 Ask Gemini"):
    if not question.strip():
        st.warning("⚠️ Please enter a question.")
    else:
        with st.spinner("🤖 Gemini is thinking..."):
            try:
                response = requests.post(API_URL, json={"question": question})
                data = response.json()

                if 'error' in data:
                    st.error("❌ " + data['error'])
                else:
                    st.session_state["last_response"] = data
                    st.success("✅ Gemini answered your question!")

            except Exception as e:
                st.error(f"❌ Request failed: {str(e)}")

# --- SHOW RESPONSE ---
if "last_response" in st.session_state:
    data = st.session_state["last_response"]
    result = data["result"]
    sql = data["sql"]
    tables_used = [tbl for tbl in ["total_sales", "ad_sales", "eligibility"] if tbl in sql]

    # --- GEMINI ANSWER DISPLAY ---
    answer = None
    if isinstance(result, list) and result and isinstance(result[0], dict):
        keys = list(result[0].keys())
        values = list(result[0].values())

        # Smart logic based on question
        if "cpc" in question.lower() and "item_id" in keys and "cpc" in keys:
            answer = f"The product with the highest CPC is <b>Item ID: {values[0]}</b>, costing <b>₹{float(values[1]):,.2f}</b> per click."
        elif "roas" in sql.lower():
            answer = f"Your Return on Ad Spend (RoAS) is ₹{float(values[0]):,.2f}"
        elif "total sales" in question.lower():
            answer = f"Your total sales is ₹{float(values[0]):,.2f}"
        else:
            pairs = [f"<b>{k}</b>: {v}" for k, v in result[0].items()]
            answer = "Here are the results:<br>" + "<br>".join(pairs)
    elif isinstance(result, str):
        answer = result
    else:
        answer = "No meaningful result returned."

    # 🎤 AI Text Output
    st.markdown("### 🤖 Gemini says:")
    st.markdown(f'<div class="gemini-box">{answer}</div>', unsafe_allow_html=True)

    # --- SQL + Table Info ---
    st.markdown("### 🧾 SQL Query Used")
    st.code(sql, language="sql")

    if tables_used:
        st.markdown(f"**📌 Tables Referenced:** `{', '.join(tables_used)}`")

    # --- VISUALIZATION + TABS ---
    if isinstance(result, list) and result:
        df = pd.DataFrame(result)
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        category_cols = df.select_dtypes(exclude='number').columns.tolist()

        tab1, tab2, tab3 = st.tabs(["📊 Visual", "📋 Table", "📘 Explanation"])

        # Visual Tab
        with tab1:
            if numeric_cols:
                chart_type = st.selectbox("Choose chart type:", [
                    "Bar Chart", "Pie Chart", "Line Chart", "Scatter Plot", "Treemap"
                ])

                fig = None
                if chart_type == "Bar Chart":
                    x = st.selectbox("X-axis", category_cols) if category_cols else None
                    y = st.selectbox("Y-axis", numeric_cols)
                    fig = px.bar(df, x=x, y=y, title=f"{y} by {x or 'Index'}")

                elif chart_type == "Pie Chart":
                    if category_cols and numeric_cols:
                        names = st.selectbox("Category", category_cols)
                        values = st.selectbox("Values", numeric_cols)
                        fig = px.pie(df, names=names, values=values)
                    else:
                        st.warning("Pie chart needs category and numeric columns.")

                elif chart_type == "Line Chart":
                    x = st.selectbox("X-axis", category_cols) if category_cols else None
                    y = st.selectbox("Y-axis", numeric_cols)
                    if x:
                        fig = px.line(df, x=x, y=y)
                    else:
                        st.warning("Line chart needs a categorical X-axis.")

                elif chart_type == "Scatter Plot":
                    x = st.selectbox("X-axis", numeric_cols)
                    y = st.selectbox("Y-axis", [col for col in numeric_cols if col != x])
                    fig = px.scatter(df, x=x, y=y)

                elif chart_type == "Treemap":
                    path = st.multiselect("Treemap Hierarchy", category_cols, default=category_cols[:1])
                    value = st.selectbox("Treemap Size", numeric_cols)
                    if path:
                        fig = px.treemap(df, path=path, values=value)

                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("ℹ️ No numeric data to visualize.")

        # Table Tab
        with tab2:
            st.dataframe(df, use_container_width=True)

        # Explanation Tab
        with tab3:
            st.markdown("This result is based on your SQL query and Gemini AI's interpretation of your question.")
