
from typing import Dict, Optional
from API.RecipeSchema import RecipeSchema, RecipeUpdate
import requests
import urllib3
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

# 3. פונקציות DB
from conection.base_func import *
from fastapi import Body
print("### API/Api.py IS RUNNING ###")

# -------------------------------
# ביטול אזהרות SSL (לוקאל)
# -------------------------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------------------
# יצירת אפליקציה
# -------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# הגדרות Gemini (עם מפתח API)
# -------------------------------
API_KEY = "AIzaSyBKwcqc311-XAaVxqWbyzFOkH-wjDreHZs"

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent?key=" + API_KEY
)

# -------------------------------
# פונקציית Gemini – REST API
# -------------------------------
def ask_gemini_chef(question: str) -> str:
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": question}]
            }
        ],
        "systemInstruction": {
            "parts": [
                {
                    "text": (
                        "אתה שף מקצועי. "
                        "ענה אך ורק על נושאים של אוכל, בישול ומתכונים. "
                        "אם השאלה לא קשורה לאוכל – "
                        "ענה בנימוס שאתה מתמחה רק במטבח."
                    )
                }
            ]
        }
    }

    try:
        response = requests.post(
            GEMINI_URL,
            json=payload,
            verify=False,
            timeout=30
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"שגיאת חיבור ל-Gemini: {e}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"שגיאה מ-Gemini: {response.text}"
        )

    try:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise HTTPException(
            status_code=500,
            detail="שגיאה בקריאת התשובה מ-Gemini"
        )

#פונקציית הצאטבוט
@app.get("/ask")
def ask(
    question: str = Query(..., description="שאלה בענייני אוכל ובישול")
):
    answer = ask_gemini_chef(question)
    return {
        "question": question,
        "answer": answer
    }

# ===============================
# RECIPES API
# ===============================
@app.get("/recipes")
def read_recipes(category: Optional[str] = None):
    if category:
        return get_recipes_by_category(category)
    return get_all_recipes()

@app.get("/recipes/{recipe_id}")
def read_recipe(recipe_id: int):
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="מתכון לא נמצא")
    return recipe


@app.post("/recipes")
def create_recipe(recipe: RecipeSchema):
    try:
        success = add_recipe(
            title=recipe.Title,
            description=recipe.Description,
            ingredients=recipe.Ingredients,
            instructions=recipe.Instructions,
            category=recipe.Category,
            prep_time=recipe.PrepTimeMinutes,
            difficulty=recipe.Difficulty,
            is_dairy=recipe.IsDairy
        )

        if success:
            return {"status": "added"}
        raise HTTPException(status_code=500, detail="Failed to add recipe")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/recipes/{recipe_id}")
def update_item(recipe_id: int, recipe_data: RecipeUpdate):
    update_dict = recipe_data.model_dump(exclude_unset=True)
    if not update_dict:



































































































        raise HTTPException(status_code=400, detail="לא נשלחו נתונים לעדכון")
    update_recipe_dynamic(recipe_id, update_dict)
    return {"status": "success", "fields": list(update_dict.keys())}


@app.delete("/recipes/{recipe_id}")
def delete_item(recipe_id: int):
    delete_recipe(recipe_id)
    return {"status": "deleted"}
