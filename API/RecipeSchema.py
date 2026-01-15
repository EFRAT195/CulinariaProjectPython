from pydantic import BaseModel
from typing import Optional

# מחלקה 1: ליצירת מתכון חדש
class RecipeSchema(BaseModel):
    Title: str
    Description: str = ""
    Ingredients: str = ""
    Instructions: str = ""
    Category: str = ""
    PrepTimeMinutes: int = 30
    Difficulty: str = "Easy"
    IsDairy: int = 0

class RecipeUpdate(BaseModel):
    Title: Optional[str] = None
    Description: Optional[str] = None
    Ingredients: Optional[str] = None
    Instructions: Optional[str] = None
    Category: Optional[str] = None
    PrepTimeMinutes: Optional[int] = None
    Difficulty: Optional[str] = None
    IsDairy: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "Title": "שם מתכון",
                "Description": "הכנס תיאור",
                "Ingredients": "",
                "Instructions": "לערבב",
                "Category": "בוקר",
                "PrepTimeMinutes": 5,
                "Difficulty": "קל",
                "IsDairy": 0
            }
        }
