from fastapi import FastAPI, HTTPException
from supabase import create_client
from dotenv import load_dotenv
import os

# -------------------- LOAD ENV --------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase environment variables not set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------- APP --------------------
app = FastAPI(
    title="GrowBox Gardening API",
    description="APIs to manage user gardens and fetch detailed plant information",
    version="1.0.0"
)

# -------------------- DUMMY USER --------------------
DUMMY_USER_ID = 101  # ONLY for testing

# -------------------- ROOT --------------------
@app.get("/")
def home():
    return {"message": "GrowBox Gardening API is running"}

# -------------------- MY GARDEN --------------------
@app.get("/my-garden")
def get_my_garden(userId: int):

    # Dummy authentication check
    if userId != DUMMY_USER_ID:
        raise HTTPException(status_code=401, detail="Unauthorized user")

    try:
        response = (
            supabase
            .table("mygarden")
            .select("PlantId, plantName, plant_image, plantedDate, categories")
            .execute()
        )

        return {
            "success": True,
            "data": response.data or []
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- PLANT DETAILS --------------------
@app.get("/plant-details/{PlantId}")
def get_plant_details(PlantId: int):

    try:
        plant_response = (
            supabase
            .table("plant_details")
            .select("*")
            .eq("PlantId", PlantId)
            .execute()
        )

        if not plant_response.data:
            raise HTTPException(status_code=404, detail="Plant not found")

        plant = plant_response.data[0]

        lifecycle_response = (
            supabase
            .table("plant_life_cycle")
            .select("*")
            .eq("Id", plant["id"])
            .order("stage_number")
            .execute()
        )

        plant["life_cycle"] = lifecycle_response.data or []

        return {
            "success": True,
            "data": plant
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
