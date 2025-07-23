# 🤖 GenAI E-commerce Assistant

An intelligent AI-powered agent that answers natural language questions related to e-commerce data — powered by Gemini AI, MySQL, and Streamlit.

> 🔍 Ask anything like “What is my total sales?” or “Which product had the highest CPC?” and get smart insights, SQL queries, and visualizations.

---

## 📦 Project Structure

```
GenAI_Ecommerce_Project/
│
├── backend/           # Flask API + Gemini integration
│   ├── run.py         # Flask app
│   ├── gemini_utils.py
│   ├── db/            
│   │   ├── .env       # Environment variables (API key, DB config)
│   │   └── requirements.txt
│
├── frontend/          # Streamlit AI Dashboard
│   └── app.py         
│
├── data/              # Provided CSV datasets (converted to MySQL)
│   ├── total_sales.csv
│   ├── ad_sales.csv
│   └── eligibility.csv
│
└── README.md
```

---

## 🚀 Features

✅ Natural language → SQL query → database result  
✅ Gemini 1.5 Flash LLM integration  
✅ Live typing effect (streaming response)  
✅ Interactive visualizations (Bar, Pie, Line, Treemap, Scatter)  
✅ Clean AI dashboard UI with dark/light themes  
✅ Tabbed layout for Visuals, Tables, and Explanations  
✅ Displays which tables were used in each query  
✅ Custom error handling for invalid inputs and expired API

---

## 🧠 Tech Stack

- **Frontend:** Streamlit, Plotly, CSS, session state
- **Backend:** Flask, SQLAlchemy, dotenv, Gemini API
- **Database:** MySQL (via MySQL Workbench)
- **LLM Used:** Gemini 1.5 Flash (via Google AI Studio)

---

## 📊 Datasets Used

The following CSV files were converted into SQL tables:

1. `total_sales` - Product-level total sales metrics  
2. `ad_sales` - Product-level ad spend & performance  
3. `eligibility` - Product eligibility status (e.g., free delivery)

---

## 🧪 Example Questions

These are supported and tested:

| Question | Response Example |
|----------|------------------|
| What is my total sales? | ₹1,004,904.56 |
| Calculate the RoAS (Return on Ad Spend) | RoAS = 2.85 |
| Which product had the highest CPC? | Product ID = 22 |
| What is the average CPC by product? | [Bar Chart shown] |
| How many customers are eligible for free delivery? | 204 customers |

---

## ⚙️ How to Run Locally

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/your-username/GenAI_Ecommerce_Project.git
cd GenAI_Ecommerce_Project
```

### 2️⃣ Setup Backend (Flask API)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r db/requirements.txt
```

Create a `.env` file inside `backend/db/` and add:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=genai_sales
GEMINI_API_KEY=your_api_key_here
```

Then run:

```bash
python run.py
```

Flask should run at `http://127.0.0.1:5000`

---

### 3️⃣ Setup Frontend (Streamlit)

In another terminal:

```bash
cd frontend
streamlit run app.py
```

---

## 🔐 How to Get Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **Create API Key**
3. Copy and paste it in `.env` under `GEMINI_API_KEY=`

> 🛑 If your key exceeds the free limit, generate a new one.

---

## 📽️ Demo Preview

> 🎥 [Video Link Here](https://drive.google.com/file/d/1VFAO0V8_lWnc2SHd_czo3cxNH0VqYYge/view?usp=sharing)  
> 📂 [GitHub Repo Link](https://github.com/abubakar07g/GenAI-E-commerce-Assistance)

---

## 🎁 Bonus Implementations

✅ Streaming text output (live typing effect)  
✅ Beautiful and interactive Streamlit UI  
✅ Chat-like answer rendering (like: “Your total sales is ₹1,004,904.56”)  
✅ Auto-detected tables used from SQL  
✅ Theme toggle & animated interface  

---



