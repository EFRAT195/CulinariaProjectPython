import pyodbc


def get_connection():
    try:
        connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-6GQSQRL\SQLEXPRESS;"
            "DATABASE=RecipesDB;"
            "Trusted_Connection=yes;"
        )
        return connection
    except Exception as e:
        print(f"שגיאה בחיבור למסד הנתונים: {e}")
        return None
conn = get_connection()

if conn:
    print("הצלחתי! החיבור למסד הנתונים של המתכונים עובד.")
    conn.close() # סוגרים את החיבור כי סיימנו לבדוק
else:
    print("החיבור נכשל.")