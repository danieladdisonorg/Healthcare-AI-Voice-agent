import os
import psycopg2
from typing import List, TypedDict
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from db import get_db_connection

# Load environment variables
load_dotenv()

# Shared LangGraph state definition
class AgentState(TypedDict):
    phrases: List[str]
    normalized_symptoms: List[str]
    specialists: List[str]
    recommended_specialists: List[str]
    doctors: List[dict]

# Initialize GPT-4
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.2,
    openai_api_key="Your_Api_Key"
)

# Normalize Agent using GPT-4
def normalize_agent(state: AgentState) -> AgentState:
    print("\nGPT-4 Normalize Agent running...")
    prompt = (
        "You are a medical assistant. Normalize the following patient symptom phrases "
        "into a list of clinical symptom terms. Only output comma-separated clinical terms.\n"
        f"Patient phrases: {state['phrases']}"
    )
    messages = [
        SystemMessage(content="You are a helpful medical assistant."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    raw_output = response.content
    normalized = [term.strip().lower() for term in raw_output.split(",") if term.strip()]
    return {"normalized_symptoms": normalized}

# Specialist Lookup Agent (via stored procedure)
def specialist_lookup_agent(state: AgentState) -> AgentState:
    print("\nLooking up specialists for:", state.get("normalized_symptoms", []))
    conn = get_db_connection()
    cur = conn.cursor()
    normalized = state.get("normalized_symptoms", [])
    if not normalized:
        cur.close()
        return {"specialists": []}

    try:
        cur.execute("SELECT * FROM sp_get_specialists(%s)", (normalized,))
        specialists = [row[0] for row in cur.fetchall()]
    except Exception as e:
        print("Error in specialist_lookup_agent:", e)
        specialists = []
    finally:
        cur.close()
        conn.close()

    return {"specialists": specialists}

# LLM-Based Specialist Recommender Agent
def recommend_specialists_agent(state: AgentState) -> AgentState:
    print("\nRecommending best specialists using GPT-4...")
    symptoms = state.get("normalized_symptoms", [])
    specialists = state.get("specialists", [])
    if not specialists or not symptoms:
        return {"recommended_specialists": []}

    prompt = (
        f"You are a medical assistant. A patient reported the following symptoms: {', '.join(symptoms)}.\n"
        f"The following specialists are available: {', '.join(specialists)}.\n"
        "From this list, which 1 or 2 specialists would be most suitable to consult first?\n"
        "Only return the recommended specialist names as a comma-separated list."
    )
    messages = [
        SystemMessage(content="You are an intelligent medical assistant that triages patients."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    raw_output = response.content
    recommended = [name.strip() for name in raw_output.split(",") if name.strip() in specialists]
    return {"recommended_specialists": recommended}

# Doctor Info Agent (via stored procedure)
def fetch_doctor_details_agent(state: AgentState) -> AgentState:
    print("\nFetching doctor info for:", state.get("recommended_specialists", []))
    recommended = state.get("recommended_specialists", [])
    if not recommended:
        return {"doctors": []}

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM sp_get_doctors_by_specialists(%s)", (recommended,))
        doctor_rows = cur.fetchall()
        doctors = []
        for row in doctor_rows:
            doctors.append({
                "doctor_id": row[0],
                "name": row[1],
                "specialization": row[2],
                "rating": float(row[3]),
                "fees": int(row[4]) if row[4] else 0,
                "hospital": row[5],
                "next_available_date": str(row[6]) if row[6] else "Not available",
                "start_time": str(row[7]) if row[7] else "N/A",
                "end_time": str(row[8]) if row[8] else "N/A",
                "slot_id": row[9]
            })
    except Exception as e:
        print("Error in fetch_doctor_details_agent:", e)
        doctors = []
    finally:
        cur.close()
        conn.close()

    return {"doctors": doctors}

# Build LangGraph flow
def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("normalize_agent", normalize_agent)
    builder.add_node("specialist_lookup_agent", specialist_lookup_agent)
    builder.add_node("recommend_specialists_agent", recommend_specialists_agent)
    builder.add_node("fetch_doctor_details_agent", fetch_doctor_details_agent)

    builder.set_entry_point("normalize_agent")
    builder.add_edge("normalize_agent", "specialist_lookup_agent")
    builder.add_edge("specialist_lookup_agent", "recommend_specialists_agent")
    builder.add_edge("recommend_specialists_agent", "fetch_doctor_details_agent")
    builder.add_edge("fetch_doctor_details_agent", END)
    return builder.compile()
