from __future__ import annotations

import os
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .db import init_db

app = FastAPI(title="AgriMitra AI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


def current_time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")


def get_demo_farmer():
    return {
        "id": "demo-user-1",
        "name": "Demo Farmer",
        "email": "demo@agrimitra.ai",
        "phone": "+91 98765 43210",
        "role": "Farmer",
        "location": "Eluru, Andhra Pradesh",
        "landArea": "5 acres",
        "soilType": "Loamy",
        "currentCrop": "Tomato",
        "cropStage": "Flowering",
        "season": "Rabi",
        "budget": "₹35,000",
        "waterStatus": "Balanced",
    }


def get_dashboard_data():
    farmer = get_demo_farmer()
    return {
        "farmer": farmer,
        "summary": {
            "farmScore": 87,
            "soilMoisture": 68,
            "temperature": 29,
            "rainfall": 18,
            "soilPH": 6.4,
            "diseaseRisk": 18,
            "irrigationStatus": "Balanced",
            "weatherSuitability": 92,
            "soilCondition": 85,
            "waterStatus": 80,
            "marketCondition": 88,
        },
        "weather": {
            "temperature": 29,
            "humidity": 68,
            "rainProbability": 62,
            "windSpeed": 13,
            "feelsLike": 32,
            "forecast": [
                {"day": "Mon", "temp": 30, "rain": 18},
                {"day": "Tue", "temp": 28, "rain": 42},
                {"day": "Wed", "temp": 31, "rain": 16},
                {"day": "Thu", "temp": 29, "rain": 26},
                {"day": "Fri", "temp": 32, "rain": 10},
                {"day": "Sat", "temp": 30, "rain": 35},
                {"day": "Sun", "temp": 29, "rain": 20},
            ],
        },
        "market": {
            "crop": "Tomato",
            "price": 2380,
            "trend": "Rising",
            "demand": "High",
            "updatedAt": current_time(),
        },
        "tasks": [
            {"title": "Irrigation review", "time": "Today · 7:30 AM", "status": "pending"},
            {"title": "Leaf inspection", "time": "Today · 11:00 AM", "status": "pending"},
            {"title": "Fertilizer check", "time": "Tomorrow · 8:00 AM", "status": "scheduled"},
        ],
        "insight": {
            "title": "AgriMitra Insight",
            "text": "Rainfall is expected within the next 24 hours. Review irrigation timing before watering the field.",
        },
        "aiRecommendation": {
            "title": "Today’s AI Recommendation",
            "message": "Based on current soil moisture, temperature and weather conditions, irrigation is not required today.",
            "confidence": "High confidence",
            "reasons": [
                "Soil moisture is within the ideal range for tomato roots.",
                "Rain probability is moderate and likely to replenish moisture.",
                "Humidity is manageable, reducing the risk of fungal pressure."
            ],
        },
        "analytics": {
            "farmHealth": [78, 80, 82, 84, 86, 88, 87],
            "soilMoisture": [60, 62, 65, 67, 63, 68, 69],
            "temperature": [28, 29, 30, 29, 31, 30, 29],
            "cropHealth": [72, 75, 78, 80, 83, 84, 87],
        },
        "alerts": [
            {"type": "Weather", "severity": "warning", "message": "High humidity may increase fungal risk in the coming 48 hours."},
            {"type": "Crop", "severity": "info", "message": "Tomato plants are approaching flowering; avoid water stress."},
            {"type": "Market", "severity": "important", "message": "Tomato demand remains strong in nearby mandis."},
        ],
    }


@app.get("/health")
async def health():
    return {"status": "ok", "service": "AgriMitra AI"}


class LoginInput(BaseModel):
    email: str
    password: str


@app.post("/api/auth/login")
async def login(payload: LoginInput):
    if payload.email == "demo@agrimitra.ai" or payload.password:
        return {
            "token": "demo-jwt-token",
            "user": get_demo_farmer(),
            "message": "Demo login successful",
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")


class RegisterInput(BaseModel):
    name: str
    email: str
    phone: str
    password: str


@app.post("/api/auth/register")
async def register(payload: RegisterInput):
    return {
        "token": "demo-jwt-token",
        "user": {
            **get_demo_farmer(),
            "name": payload.name,
            "email": payload.email,
            "phone": payload.phone,
        },
        "message": "Profile created successfully",
    }


@app.post("/api/auth/forgot-password")
async def forgot_password(payload: Dict[str, str]):
    email = payload.get("email")
    return {
        "message": f"Password reset link sent to {email or 'your email'}.",
        "demoMode": True,
    }


@app.get("/api/profile")
async def get_profile():
    return get_demo_farmer()


@app.get("/api/farms")
async def get_farms():
    return [{
        "id": "field-1",
        "name": "Main Field",
        "location": "Eluru, AP",
        "area": "5 acres",
        "soilType": "Loamy",
        "irrigation": "Drip",
        "water": "Moderate",
        "previousCrop": "Rice",
        "crop": "Tomato",
        "stage": "Flowering",
    }]


@app.get("/api/dashboard")
async def dashboard():
    return get_dashboard_data()


class CropRecommendationInput(BaseModel):
    location: str = "Eluru, Andhra Pradesh"
    landArea: str = "5 acres"
    soilType: str | None = "Loamy"
    nitrogen: int | None = None
    phosphorus: int | None = None
    potassium: int | None = None
    ph: float | None = None
    temperature: int = 30
    humidity: int = 68
    rainfall: int = 900
    waterAvailability: str = "Moderate"
    previousCrop: str = "Rice"
    season: str = "Rabi"
    budget: str = "₹35,000"
    hasSoilReport: bool = False
    soilReportSource: str = "No soil report"


@app.post("/api/crop-recommendation/recommend")
async def recommend_crop(payload: CropRecommendationInput):
    soilDataStatus = "Values were extracted from the uploaded soil test report." if payload.hasSoilReport else "No soil test report was uploaded. N, P, K, and pH values are not available."
    recommendationType = "Preliminary Recommendation" if not payload.hasSoilReport else "Recommendation based on uploaded soil report"
    notes = [
        "No soil test report was uploaded, so this is a preliminary recommendation.",
        "A recognized soil test can improve nutrient and pH accuracy before final fertilizer planning.",
    ] if not payload.hasSoilReport else [
        "Nutrient values were reviewed from the uploaded soil report.",
        "Values should still be verified against the latest laboratory analysis before final fertilization decisions.",
    ]

    recommendations = [
        {
            "name": "Tomato",
            "suitability": 94,
            "why": ["Suitable for loamy soil and moderate rainfall", "Matches the current heat and humidity range", "Fits your budget and Rabi season"],
            "waterNeed": "Moderate to high",
            "soilNeed": "Well-drained loam with balanced organic matter",
            "temperatureNeed": "22-32°C",
            "duration": "90-120 days",
            "season": "Rabi / Kharif transition",
            "stages": ["Seedling", "Vegetative growth", "Flowering", "Fruit development", "Harvest"],
            "resourceRequirements": {"water": "Drip irrigation recommended", "fertilizer": "Balanced NPK with micronutrients", "labor": "Moderate"},
            "marketNote": "High local demand in nearby mandis and urban clusters",
        },
        {
            "name": "Chilli",
            "suitability": 88,
            "why": ["Good with warm conditions and moderate irrigation", "Well suited to loamy fields with good drainage", "Strong market demand in regional markets"],
            "waterNeed": "Moderate",
            "soilNeed": "Loam or sandy loam",
            "temperatureNeed": "25-35°C",
            "duration": "120-150 days",
            "season": "Rabi",
            "stages": ["Nursery", "Transplanting", "Flowering", "Fruit setting", "Harvest"],
            "resourceRequirements": {"water": "Regular but controlled irrigation", "fertilizer": "NPK with potash", "labor": "Moderate"},
            "marketNote": "Illustrative market assessment for demo purposes",
        },
        {
            "name": "Groundnut",
            "suitability": 82,
            "why": ["Matches well-drained soils and dry spells", "Useable when rainfall is moderate but consistent", "Good rotation option after paddy"],
            "waterNeed": "Low to moderate",
            "soilNeed": "Sandy loam or loam",
            "temperatureNeed": "20-30°C",
            "duration": "100-130 days",
            "season": "Kharif",
            "stages": ["Sowing", "Vegetative phase", "Pegging", "Pod formation", "Harvest"],
            "resourceRequirements": {"water": "Irrigation only during dry stress", "fertilizer": "Phosphorus-rich", "labor": "Moderate"},
            "marketNote": "Illustrative crop plan and not financial advice",
        },
    ]
    return {
        "recommendedCrop": recommendations[0],
        "alternatives": recommendations[1:],
        "model": "Demo Random Forest / Rule-based fallback",
        "confidence": "Demo model suitability score",
        "generatedAt": current_time(),
        "recommendationType": recommendationType,
        "soilDataStatus": soilDataStatus,
        "notes": notes,
    }


@app.get("/api/weather")
async def weather():
    return {
        "current": {
            "temperature": 29,
            "feelsLike": 32,
            "humidity": 68,
            "rainfall": 18,
            "windSpeed": 13,
            "rainProbability": 62,
            "updatedAt": current_time(),
        },
        "forecast": [
            {"day": "Mon", "temp": 30, "rain": 18, "condition": "Partly cloudy"},
            {"day": "Tue", "temp": 28, "rain": 42, "condition": "Rain likely"},
            {"day": "Wed", "temp": 31, "rain": 16, "condition": "Sunny"},
            {"day": "Thu", "temp": 29, "rain": 26, "condition": "Mixed"},
            {"day": "Fri", "temp": 32, "rain": 10, "condition": "Sunny"},
            {"day": "Sat", "temp": 30, "rain": 35, "condition": "Rain shower"},
            {"day": "Sun", "temp": 29, "rain": 20, "condition": "Cloudy"},
        ],
        "actions": [
            {"title": "Rain expected", "advice": "Review irrigation before the next watering cycle.", "severity": "info"},
            {"title": "High humidity", "advice": "Inspect leaves for fungal symptoms in the next 24-48 hours.", "severity": "warning"},
            {"title": "Strong wind", "advice": "Avoid spraying in windy conditions if possible.", "severity": "warning"},
        ],
        "farmingImpact": {
            "irrigation": {"status": "Not required", "detail": "Soil moisture remains within the recommended range for tomato roots."},
            "spraying": {"status": "Suitable", "detail": "Morning hours are better for application before heavier clouds build later."},
            "diseaseRisk": {"status": "Low to medium", "detail": "Humidity is elevated, so leaf and fungal checks are still recommended."},
            "rainRisk": {"status": "Medium", "detail": "Moderate rain chance may benefit the field but could delay routine spray work."}
        },
        "source": "Demo weather fallback",
    }


@app.get("/api/market")
async def market():
    return {
        "selectedCrop": "Tomato",
        "selectedLocation": "Eluru Mandi",
        "price": 2380,
        "trend": [2200, 2285, 2340, 2420, 2470, 2380],
        "comparisons": [
            {"market": "Eluru", "price": 2380},
            {"market": "Vijayawada", "price": 2310},
            {"market": "Rajahmundry", "price": 2445},
            {"market": "Tadepalligudem", "price": 2365},
        ],
        "demand": "High",
        "updatedAt": current_time(),
        "demoData": True,
    }


@app.get("/api/calendar")
async def calendar():
    return {
        "crop": "Tomato",
        "timeline": [
            {"name": "Seed Preparation", "status": "completed"},
            {"name": "Land Preparation", "status": "completed"},
            {"name": "Sowing", "status": "completed"},
            {"name": "Germination", "status": "completed"},
            {"name": "Vegetative Growth", "status": "in-progress"},
            {"name": "Flowering", "status": "pending"},
            {"name": "Fruit Development", "status": "pending"},
            {"name": "Harvest", "status": "pending"},
        ],
        "recommendedActivities": [
            "Monitor leaf health for early blight signs",
            "Check soil moisture before evening irrigation",
            "Review nutrient application for flowering stage",
        ],
    }


@app.post("/api/calendar/task")
async def add_task(payload: Dict[str, Any]):
    return {"message": "Task added successfully", "task": payload}


@app.get("/api/chat")
async def chat_history():
    return {
        "messages": [
            {"role": "assistant", "text": "Hello! I can help with crop selection, weather-driven actions, and field care."},
            {"role": "user", "text": "Which crop is suitable for my soil?"},
            {"role": "assistant", "text": "Based on your loamy soil, moderate rainfall, and current season, tomato is a strong fit with a demo suitability score of 94%."},
        ]
    }


@app.post("/api/chat")
async def send_chat(payload: Dict[str, str]):
    question = payload.get("message", "")
    q = question.lower()
    farmer = get_demo_farmer()
    weather_data = await weather()
    current = weather_data["current"]

    if "crop" in q and ("grow" in q or "suitable" in q or "soil" in q):
        response = f"Based on your {farmer['soilType']} soil, {farmer['currentCrop']} is the most suitable crop for this season, with a strong suitability score and good fit for your current rainfall and temperature profile."
    elif "yellow" in q:
        response = "Yellowing can be caused by nutrient stress, overwatering, or early disease stress. Your current humidity and rainfall pattern make it wise to inspect the lower leaves and check drainage before adding more fertilizer."
    elif "irrigate" in q:
        response = f"Based on your current soil moisture and weather conditions ({current['temperature']}°C, {current['humidity']}% humidity, {current['rainProbability']}% rain chance), irrigation is not urgently required today. Re-check soil moisture tomorrow morning if rainfall remains low."
    elif "disease" in q or "risk" in q:
        response = "Current conditions suggest a low-to-medium fungal disease risk because humidity is elevated. Continue regular leaf checks and avoid late-evening spraying if rain is expected."
    elif "rain" in q:
        response = f"Rain is likely in the next 24-48 hours ({current['rainProbability']}% chance), so it is a good time to delay heavy irrigation and protect the field from unnecessary water stress."
    elif "fertil" in q or "yield" in q or "improve" in q:
        response = "To improve yield, keep soil pH between 6.0 and 6.8, maintain steady moisture at flowering, and use balanced NPK feeding based on your crop stage."
    else:
        response = "AgriMitra can support crop planning, weather actions, disease checks, and farm scheduling. Share your field condition and I’ll help recommend the next step for your farm."
    return {"reply": response, "demoMode": True}


@app.get("/api/knowledge")
async def knowledge():
    return {
        "categories": ["Crops", "Soil", "Irrigation", "Fertilizers", "Diseases", "Pests", "Weather", "Harvest"],
        "featured": [
            {"title": "Soil health for tomato fields", "category": "Soil", "summary": "Keep root-zone moisture balanced and maintain organic matter for healthy flowering."},
            {"title": "Drip irrigation planning", "category": "Irrigation", "summary": "Timing irrigation by weather and crop stage lowers water stress and saves resources."},
            {"title": "Early blight recognition", "category": "Diseases", "summary": "Look for concentric leaf spots and rapid spread under high humidity."},
        ],
        "articles": [
            {"id": "a1", "title": "Crop planning for Rabi vegetables", "category": "Crops", "summary": "Plan for irrigation, nutrient timing, and disease prevention."},
            {"id": "a2", "title": "Balancing nutrients in loamy soil", "category": "Soil", "summary": "Use soil testing and crop-stage based nutrient application."},
            {"id": "a3", "title": "When to inspect for fungal stress", "category": "Diseases", "summary": "High humidity and wet evenings are common triggers for fungal symptoms."},
        ],
        "faqs": [
            {"q": "How do I know when to irrigate?", "a": "Check soil moisture, weather forecast, and plant stress signs as a combined decision."},
            {"q": "What should I inspect during flowering?", "a": "Look for nutrient imbalance, pollination issues, and early leaf diseases."},
        ],
    }


@app.get("/api/insights")
async def insights():
    return {
        "items": [
            {"title": "Weather Insight", "severity": "info", "reason": "Rain expected tomorrow.", "action": "Delay irrigation and monitor root-zone moisture.", "timestamp": current_time()},
            {"title": "Crop Insight", "severity": "info", "reason": "Tomato crop is approaching flowering.", "action": "Keep nutrient and moisture balance steady.", "timestamp": current_time()},
            {"title": "Health Insight", "severity": "warning", "reason": "Humidity may raise fungal risk.", "action": "Inspect foliage during evening checks.", "timestamp": current_time()},
            {"title": "Market Insight", "severity": "important", "reason": "Demand remains high in local mandis.", "action": "Prepare harvesting and packaging timing.", "timestamp": current_time()},
        ]
    }


@app.get("/api/reports")
async def reports():
    return {
        "summary": {
            "farmer": get_demo_farmer()["name"],
            "location": "Eluru, Andhra Pradesh",
            "currentCrop": "Tomato",
            "cropStage": "Flowering",
            "status": "Healthy with low disease risk",
        },
        "reportSections": [
            "Farmer profile",
            "Farm information",
            "Current crop",
            "Crop recommendation",
            "Disease history",
            "Weather summary",
            "Market information",
            "Smart insights",
        ],
        "demoMode": True,
        "updatedAt": current_time(),
    }


@app.get("/api/notifications")
async def notifications():
    return [
        {"id": "n1", "type": "Weather alert", "severity": "warning", "message": "Rain expected by tomorrow morning."},
        {"id": "n2", "type": "Crop task", "severity": "info", "message": "Review irrigation schedule before evening."},
        {"id": "n3", "type": "Disease warning", "severity": "important", "message": "High humidity may favor early blight risk."},
        {"id": "n4", "type": "Market update", "severity": "info", "message": "Tomato prices are trending upward in Eluru mandi."},
    ]


@app.get("/api/demo")
async def demo_data():
    return {
        "demoMode": True,
        "message": "AgriMitra AI is running in demo mode with sample farm data.",
        "farmer": get_demo_farmer(),
        "dashboard": get_dashboard_data(),
    }


@app.post("/api/disease-detection/analyze")
async def analyze_disease(file: UploadFile = File(default=None), imageUrl: str = Form(default="")):
    if file is None and not imageUrl:
        return {
            "disease": "Early Blight",
            "confidence": 94.6,
            "symptoms": ["Dark concentric leaf spots", "Yellowing around lesions", "Spread under humid conditions"],
            "possibleCauses": ["High humidity", "Poor air circulation", "Leaf wetness"],
            "actions": ["Avoid overhead watering", "Improve spacing and ventilation", "Remove affected leaves if severe"],
            "prevention": ["Use resistant varieties when available", "Inspect fields after evening rain", "Rotate crops in future cycles"],
            "consultExpert": True,
            "demoMode": True,
        }

    if file is not None:
        return {
            "disease": "Early Blight",
            "confidence": 94.6,
            "symptoms": ["Dark concentric leaf spots", "Yellowing around lesions", "Spread under humid conditions"],
            "possibleCauses": ["High humidity", "Poor air circulation", "Leaf wetness"],
            "actions": ["Avoid overhead watering", "Improve spacing and ventilation", "Remove affected leaves if severe"],
            "prevention": ["Use resistant varieties when available", "Inspect fields after evening rain", "Rotate crops in future cycles"],
            "consultExpert": True,
            "demoMode": True,
        }

    return {
        "disease": "Early Blight",
        "confidence": 94.6,
        "symptoms": ["Dark concentric leaf spots", "Yellowing around lesions", "Spread under humid conditions"],
        "possibleCauses": ["High humidity", "Poor air circulation", "Leaf wetness"],
        "actions": ["Avoid overhead watering", "Improve spacing and ventilation", "Remove affected leaves if severe"],
        "prevention": ["Use resistant varieties when available", "Inspect fields after evening rain", "Rotate crops in future cycles"],
        "consultExpert": True,
        "demoMode": True,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
