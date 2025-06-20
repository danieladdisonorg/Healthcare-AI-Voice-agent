from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from config import Config
from db import get_db_connection
from models import LoginRequest, AppointmentRequest
from preprocess import preprocess_text
from queries import *
from langgraph_llm_agents import build_graph
from models import PatientDetailsResponse
from models import MedicalHistoryResponse

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = get_db_connection()


@app.get("/")
async def root():
    return {"message": "Welcome to the Healthcare Agent API!"}

@app.post("/login")
def login(request: LoginRequest):
    logger.info(f"Login attempt: {request.email} / {request.password}")
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM sp_login_user(%s::TEXT, %s::TEXT)", (request.email, request.password))
        user = cur.fetchone()
        cur.close()
    except Exception as e:
        logger.error(f"Database error during login: {e}")
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail="Login failed")

    if user:
        return JSONResponse(content={"message": "Login successful", "user_id": user[0]})
    
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/patient-details/{user_id}", response_model=PatientDetailsResponse)
def get_patient_details(user_id: int):
    logger.info(f"Fetching patient details for user_id={user_id}")
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM sp_get_patient_details(%s);", (user_id,))
        row = cur.fetchone()
        logger.info(f"Fetched row: {row}")
        cur.close()
    except Exception as e:
        logger.error(f"DB error in patient-details: {e}")
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    if row:
        return jsonable_encoder({
            "name": row[0], "date_of_birth": row[1], "gender": row[2], "contact_number": row[3],
            "medical_record_number": row[4], "blood_group": row[5], "marital_status": row[6], "id": row[7]
        })
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/medical-history/{user_id}", response_model=MedicalHistoryResponse)
def get_medical_history(user_id: int):
    logger.info(f"Fetching medical history for user_id={user_id}")
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM sp_get_patient_id(%s);", (user_id,))
        patient_row = cur.fetchone()
        logger.info(f"Patient row: {patient_row}")
        if not patient_row:
            cur.close()
            raise HTTPException(status_code=404, detail="Patient not found")
        patient_id = patient_row[0]

        cur.execute("SELECT * FROM sp_get_medical_history(%s);", (patient_id,))
        row = cur.fetchone()
        logger.info(f"Medical history row: {row}")
        cur.close()
    except Exception as e:
        logger.error(f"DB error in medical-history: {e}")
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    if row:
        return jsonable_encoder({
            "past_diagnoses": row[0], "surgeries": row[1], "hospital_admissions": row[2],
            "immunization_records": row[3], "family_medical_history": row[4], "lifestyle_factors": row[5]
        })
    raise HTTPException(status_code=404, detail="Medical history not found")

@app.post("/normalize")
async def normalize(request: Request):
    data = await request.json()
    phrases = data.get("phrases", [])
    results = []
    for phrase in phrases:
        cleaned = preprocess_text(phrase)
        if not cleaned:
            continue
        emb = model.encode([cleaned])
        D, I = index.search(np.array(emb), 1)
        distance = D[0][0]
        match = terms[I[0][0]]
        if distance > 1.0:
            continue
        results.append({"original": phrase, "cleaned": cleaned, "match": match, "score": float(distance)})
    return {"results": results}

@app.post("/run_langgraph")
async def run_langgraph(request: Request):
    data = await request.json()
    phrases = data.get("phrases", [])
    if not phrases:
        raise HTTPException(status_code=400, detail="No phrases provided.")
    graph = build_graph()
    final_state = graph.invoke({"phrases": phrases})
    return {
        "phrases": final_state.get("phrases", []),
        "normalized_symptoms": final_state.get("normalized_symptoms", []),
        "specialists": final_state.get("specialists", []),
        "recommended_specialists": final_state.get("recommended_specialists", []),
        "doctors": final_state.get("doctors", [])
    }

@app.post("/appointments")
def create_appointment(req: AppointmentRequest):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM sp_create_appointment(%s, %s, %s, %s)", (req.patient_id, req.doctor_id, req.slot_id, req.reason))
        appointment_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return {"message": "Appointment created", "appointment_id": appointment_id}
    except Exception as e:
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail=str(e))