from fastapi import FastAPI, HTTPException
from supabase import create_client
from dotenv import load_dotenv
import os

# ---------------- ENV ----------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="GrowBox Gardening API",
    description="APIs to manage user gardens and fetch plant details with life cycle",
    version="1.0.0"
)

# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {
        "status": "healthy",
        "service": "GrowBox Gardening API",
        "version": "1.0.0"
    }

# ---------------- MY GARDEN (FULL DATA) ----------------
@app.get("/my-garden")
def get_my_garden(userId: int):
    """
    Fetch all plants planted by user
    Then fetch plant details + lifecycle for each plant
    """

    # 1. Get user plants
    garden_res = (
        supabase
        .table("mygarden")
        .select("*")
        .eq("user_id", userId)
        .execute()
    )

    if not garden_res.data:
        return {"success": True, "data": []}

    final_plants = []

    # 2. For each plant in garden
    for plant in garden_res.data:
        plant_id = plant["PlantId"]

        # 3. Fetch plant details
        details_res = (
            supabase
            .table("plant_details")
            .select("*")
            .eq("PlantId", plant_id)
            .execute()
        )

        if not details_res.data:
            continue

        plant_details = details_res.data[0]

        # 4. Fetch life cycle using plant_details.id
        lifecycle_res = (
            supabase
            .table("plant_lifecycle")
            .select("*")
            .eq("Id", plant_details["id"])
            .order("stage_number")
            .execute()
        )

        plant_details["life_cycle"] = lifecycle_res.data

        # 5. Merge garden + details
        final_plants.append({
            "my_garden": plant,
            "plant_details": plant_details
        })

    return {
        "success": True,
        "data": final_plants
    }

# ---------------- SINGLE PLANT DETAILS ----------------
@app.get("/plant-details/{PlantId}")
def get_plant_details(PlantId: int):

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
