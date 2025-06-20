# 🩺 AI Healthcare Voice Assistant

A comprehensive full-stack healthcare application that leverages AI-powered voice interactions for patient triage, symptom analysis, specialist mapping, and appointment booking. Built with modern technologies including FastAPI, PostgreSQL, React, and integrated with leading AI models.

---

## 🌟 Overview

This healthcare AI assistant streamlines the patient care journey by providing:
- **Intelligent Voice Triage**: Natural language symptom collection and analysis
- **AI-Powered Diagnosis**: Advanced symptom normalization and specialist recommendation
- **Smart Doctor Matching**: Automated healthcare provider lookup based on specialization
- **Seamless Booking**: Integrated appointment scheduling with payment processing
- **Conversational Interface**: Intuitive voice-enabled user experience

---

## ✨ Key Features

### 🎤 Voice-Enabled Interaction
- Real-time speech-to-text conversion using Web Speech API
- Natural language processing for symptom collection
- Voice-guided patient triage workflow

### 🤖 AI-Powered Medical Intelligence
- Integration with Gemini and GPT-4 for symptom analysis
- LangGraph-based symptom normalization
- Intelligent specialist mapping and recommendations

### 🏥 Healthcare Management
- Comprehensive doctor database with specialization filtering
- PostgreSQL-powered efficient data retrieval
- Automated appointment scheduling system

### 💳 Payment Integration
- Secure payment processing via Razorpay
- Test mode support for development
- Transaction management and tracking

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | React, CSS, JavaScript | User interface and voice interactions |
| **Backend** | FastAPI, Python | API services and business logic |
| **AI/ML** | Gemini, GPT-4, LangGraph | Natural language processing and AI agents |
| **Database** | PostgreSQL | Data persistence and stored procedures |
| **Voice** | Web Speech API | Speech recognition and synthesis |
| **Payments** | Razorpay | Payment processing and gateway |
| **Deployment** | Uvicorn, Vite | Development and production servers |

---

## 📂 Project Architecture

```
healthcare-ai-assistant/
├── backend/                    # FastAPI backend services
│   ├── main.py                # Application entry point
│   ├── agents/                # LangGraph AI agents
│   ├── db/                    # Database connections and queries
│   ├── models.py              # Data models and schemas
│   ├── config.py              # Configuration management
│   └── .env                   # Environment variables (excluded from git)
│
├── frontend/                   # React frontend application
│   ├── components/            # Reusable UI components
│   ├── pages/                 # Application pages/views
│   └── .env.local             # Frontend environment variables
│
├── sql/                       # Database schema and functions
│   ├── schema.sql             # Database table definitions
│   └── functions/             # PostgreSQL stored procedures
│       ├── create_login_function.sql
│       ├── create_appointment_function.sql
│       ├── get_patient_details.sql
│       └── get_doctors_by_specialist.sql
│
├── requirements.txt           # Python dependencies
├── package.json              # Node.js dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **PostgreSQL 12+**
- **Git**

### 1. 🗄️ Database Setup

#### Create Database and User
```bash
psql -U postgres
```

```sql
CREATE DATABASE healthcare;
CREATE USER fastapi_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE healthcare TO fastapi_user;
\q
```

#### Initialize Schema and Functions
```bash
psql -U fastapi_user -d healthcare -f sql/schema.sql
```

```bash
psql -U fastapi_user -d healthcare -f sql/functions/create_login_function.sql
```

```bash
psql -U fastapi_user -d healthcare -f sql/functions/create_appointment_function.sql
```

```bash
psql -U fastapi_user -d healthcare -f sql/functions/get_patient_details.sql
```

```bash
psql -U fastapi_user -d healthcare -f sql/functions/get_doctors_by_specialist.sql
```

### 2. 🔧 Backend Configuration

#### Setup Virtual Environment
```bash
cd backend
```

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Environment Configuration
Create `.env` file in the `backend/` directory:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=fastapi_user
DB_PASSWORD=your_secure_password
DB_NAME=healthcare

# CORS Configuration
FRONTEND_ORIGIN=http://localhost:5173

# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

#### Start Backend Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 🎨 Frontend Setup

#### Install Dependencies
```bash
npm install
```

#### Environment Configuration
Create `.env.local` file in the root directory:

```env
# API Configuration
VITE_BACKEND_URL=http://localhost:8000
VITE_GEMINI_API_KEY=your_gemini_api_key_here

# Payment Configuration
VITE_RAZORPAY_KEY_ID=your_razorpay_key_id_here
```

#### Start Development Server
```bash
npm run dev
```

### 4. 💳 Payment Setup (Optional)

1. Create a [Razorpay account](https://razorpay.com/)
2. Navigate to API Keys section in dashboard
3. Copy the Key ID and Key Secret
4. Update the payment configuration in `frontend/components/Recommendation.jsx`

---

## 🔑 API Keys Setup

### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and navigate to API Keys
3. Generate a new secret key
4. Add to backend `.env` file

### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Create a new project or select existing
3. Generate API key
4. Add to both backend `.env` and frontend `.env.local`

### Razorpay Configuration
1. Sign up at [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Switch to Test Mode for development
3. Copy API keys from Settings > API Keys
4. Configure in frontend environment

---

## 🏃‍♂️ Running the Application

1. **Start PostgreSQL service**
2. **Launch Backend**: `uvicorn main:app --reload` (from `backend/` directory)
3. **Launch Frontend**: `npm run dev` (from root directory)
4. **Access Application**: Navigate to `http://localhost:5173`

---

## 🧪 Testing

### Backend API Testing
```bash
curl http://localhost:8000/health
```

### Database Connection Testing
```bash
python -c "from backend.db.connection import get_db_connection; print('DB Connected!' if get_db_connection() else 'DB Connection Failed!')"
```

---

## 🚀 Deployment

### Backend Deployment
- Configure production database credentials
- Set up environment variables on hosting platform
- Deploy using platforms like Heroku, Railway, or DigitalOcean

### Frontend Deployment
- Build production bundle: `npm run build`
- Deploy to Vercel, Netlify, or similar platforms
- Update CORS settings in backend for production domain

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check existing documentation and FAQs
- Review the troubleshooting section below

---

## 🔧 Troubleshooting

### Common Issues

**Database Connection Error**
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database and user exist

**Voice Recognition Not Working**
- Use HTTPS or localhost only
- Check browser microphone permissions
- Verify Web Speech API support

**API Key Errors**
- Validate API keys are correctly set
- Check for trailing spaces or quotes
- Verify API key permissions and quotas

---

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Mobile application development
- [ ] Advanced AI model integration
- [ ] Telemedicine video consultation
- [ ] Electronic health records integration
- [ ] Real-time chat support
- [ ] Advanced analytics dashboard

---

**Built with ❤️ for better healthcare accessibility**
