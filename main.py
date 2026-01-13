from fastapi import FastAPI, HTTPException
from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize FastAPI app
app = FastAPI(
    title="GrowBox Plant API",
    description="API for fetching plant data from Supabase",
    version="1.0.0"
)

# -------------------- ROOT --------------------
@app.get("/")
def home():
    return {"message": "Plant API is running"}

# -------------------- GET ALL PLANTS --------------------
@app.get("/plants")
def get_plants():
    response = supabase.table("mygarden").select("*").execute()
    return response.data

# -------------------- GET PLANT BY ID --------------------
@app.get("/plants/{plant_id}")
def get_plant_by_id(plant_id: int):
    response = (
        supabase
        .table("mygarden")
        .select("*")
        .eq("PlantId", plant_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Plant not found")

    return response.data

# -------------------- GET PLANT BY NAME (OPTIONAL) --------------------
@app.get("/plants/by-name/{plant_name}")
def get_plant_by_name(plant_name: str):
    response = (
        supabase
        .table("mygarden")
        .select("*")
        .ilike("plantName", f"%{plant_name}%")
        .execute()
    )
    return response.data
