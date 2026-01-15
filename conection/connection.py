#this is a demo connection the real connection is to the SQL

recipes = [
    {
        "RecipeId": 1,
        "Title": "עוגת שוקולד רכה",
        "Description": "עוגת שוקולד גבוהה ואוורירית שמתאימה לאירוח",
        "Ingredients": "2 כוסות קמח, 1 כוס סוכר, 3 ביצים, חצי כוס קקאו, כוס מים חמים",
        "Instructions": "מערבבים חומרים יבשים, מוסיפים ביצים ונוזלים, אופים 40 דקות ב-170 מעלות",
        "Category": "עוגות",
        "PrepTimeMinutes": 60,
        "Difficulty": "Medium",
        "IsDairy": 1
    },
    {
        "RecipeId": 2,
        "Title": "מרק ירקות חורפי",
        "Description": "מרק מחמם ובריא לימי החורף",
        "Ingredients": "גזר, תפוח אדמה, קישוא, בצל, סלרי, מלח, פלפל",
        "Instructions": "קוצצים ירקות, מבשלים כשעה עד ריכוך מלא",
        "Category": "מרקים",
        "PrepTimeMinutes": 50,
        "Difficulty": "Easy",
        "IsDairy": 0
    },
    # הוסיפי את כל המתכונים שהיו ברשימה שלך
]

def get_connection():
    # מחזיר חיבור מזויף שמדמה מסד נתונים
    class DummyConn:
        def cursor(self):
            return self
        def execute(self, sql, params=None):
            return self
        def fetchall(self):
            return [tuple(r.values()) for r in recipes]
        def fetchone(self):
            return tuple(recipes[0].values())
        def close(self):
            pass
        @property
        def description(self):
            return [(k,) for k in recipes[0].keys()]
        def commit(self):
            pass
    return DummyConn()
