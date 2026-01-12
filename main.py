from fastapi import FastAPI, HTTPException
from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase credentials not found in .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="GrowBox Gardening API",
    description="APIs to fetch user garden plants and plant details",
    version="1.0.0"
)


# -------------------------
# Root Health Check
# -------------------------
@app.get("/")
def home():
    return {
        "status": "healthy",
        "service": "GrowBox Gardening API",
        "version": "1.0.0"
    }


# -------------------------
# My Garden (Demo Mode)
# -------------------------
@app.get("/my-garden")
def get_my_garden():
    """
    Demo mode:
    Fetch all plants from mygarden table
    """

    garden_res = supabase.table("mygarden").select("*").execute()

    if not garden_res.data:
        return {
            "success": True,
            "data": []
        }

    return {
        "success": True,
        "data": garden_res.data
    }


# -------------------------
# Plant Details + Life Cycle
# -------------------------
@app.get("/plant-details/{PlantId}")
def get_plant_details(PlantId: int):
    """
    Fetch plant details and lifecycle using PlantId
    """

    # Fetch plant details
    details_res = (
        supabase
        .table("plant_details")
        .select("*")
        .eq("PlantId", PlantId)
        .execute()
    )

    if not details_res.data:
        raise HTTPException(status_code=404, detail="Plant not found")

    plant_details = details_res.data[0]

    # Fetch lifecycle stages
    lifecycle_res = (
        supabase
        .table("plant_lifecycle")
        .select("*")
        .eq("Id", plant_details["id"])
        .order("stage_number")
        .execute()
    )

    plant_details["life_cycle"] = lifecycle_res.data

    return {
        "success": True,
        "data": plant_details
    }
