from fastapi import FastAPI
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Plant API")

@app.get("/")
def home():
    return {"message": "Plant API is running"}

@app.get("/plants")
def get_plants():
    data = supabase.table("mygarden").select("*").execute()
    return data.data

@app.get("/plants/{plant_id}")
def get_plant_by_id(plant_id: int):
    data = supabase.table("mygarden").select("*").eq("PlantId", plant_id).execute()
    return data.data

