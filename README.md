# 🩺 AI Healthcare Assistant

A full-stack voice-enabled AI medical assistant that conducts patient triage, maps symptoms to specialists using LLM, retrieves matching doctors, and enables appointment booking — using FastAPI backend, PostgreSQL, and React frontend.

---

## 🚀 Features

- Voice-based symptom triage with Gemini/GPT-4
- Symptom normalization and specialist mapping via LangGraph
- Doctor lookup from PostgreSQL using stored functions
- Appointment booking through Razorpay
- Conversational UI powered by React + JavaScript Speech APIs

---

## 🛠️ Tech Stack

| Layer       | Technology               |
|-------------|--------------------------|
| Frontend    | React, CSS               |
| Backend     | FastAPI, LangGraph       |
| AI Models   | Gemini / GPT-4           |
| Voice       | JS Web Speech API        |
| Database    | PostgreSQL               |
| Payment     | Razorpay (test mode)     |

---

## 📁 Project Structure

healthcare-ai-assistant/
│
├── backend/ # FastAPI backend
│ ├── main.py
│ ├── agents/ # LangGraph agents
│ ├── db/ # DB queries and connection
│ ├── .env # Environment variables (not pushed)
| |---.config.py
| |---models.py
├── requirements.txt # Python dependencies
│
├── frontend/ # React frontend--- here I have not created separate folder for frontend
│ ├── components/
│ ├── pages/
│ └── .env.local # API keys and backend URL
│
├── sql/ # PostgreSQL schema and stored functions
│ ├── schema.sql
│ └── functions/
│ ├── create_login_function.sql
│ ├── create_appointment_function.sql
│ ├── get_patient_details.sql
│ ├── get_doctors_by_specialist.sql
│
├── .gitignore
└── README.md


---

## ⚙️ Getting Started

### ✅ 1. PostgreSQL Setup
I
1. **Create Database & User:**

```sql
CREATE DATABASE healthcare;
CREATE USER fastapi_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE healthcare TO fastapi_user;

2. Run Schema
psql -U fastapi_user -d healthcare -f sql/schema.sql

3 Run stored functions:
psql -U fastapi_user -d healthcare -f sql/functions/create_login_function.sql
psql -U fastapi_user -d healthcare -f sql/functions/create_appointment_function.sql
psql -U fastapi_user -d healthcare -f sql/functions/get_patient_details.sql
psql -U fastapi_user -d healthcare -f sql/functions/get_doctors_by_specialist.sql

II
1. Backend Setup (FastAPI)
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

2.  Create .env in backend/

DB_HOST=localhost
DB_PORT=5432
DB_USER=fastapi_user
DB_PASSWORD=yourpassword
DB_NAME=healthcare
FRONTEND_ORIGIN=http://localhost:5173

Get openAI key and paste here

3. Start the FastAPI server:
uvicorn main:app --reload

III
1. Frontend Setup (React)
npm install

2. Create .env.local 
VITE_GEMINI_API_KEY=your_real_gemini_api_key_here
VITE_BACKEND_URL=http://localhost:8000

3. Start the frontend:
npm run dev

# For razorpay-- create account and use that secretkey in Recommendation.jsx handlepayment function

