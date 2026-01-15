from conection.connection import get_connection

def get_all_recipes():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Recipes")
    columns = [c[0] for c in cursor.description]
    recipes = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return recipes


def get_recipe_by_id(recipe_id: int):
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Recipes WHERE RecipeId = ?", (recipe_id,))
        row = cursor.fetchone()
        if not row:
            return None
        columns = [c[0] for c in cursor.description]
        recipe = dict(zip(columns, row))
        return recipe
    except Exception as e:
        print(f"שגיאה ב-get_recipe_by_id: {e}")
        return None
    finally:
        conn.close()
def add_recipe(title, description, ingredients, instructions, category, prep_time, difficulty, is_dairy):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    sql = """
        INSERT INTO Recipes (Title, Description, Ingredients, Instructions, Category, PrepTimeMinutes, Difficulty, IsDairy)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        cursor.execute(sql, (title, description, ingredients, instructions, category, prep_time, difficulty, is_dairy))
        conn.commit()
        return True
    except Exception as e:
        print(f"SQL Error: {e}")
        return False
    finally:
        conn.close()

def update_recipe_dynamic(recipe_id, data_to_update):
    if not data_to_update: return
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        set_clause = ", ".join([f"{col} = ?" for col in data_to_update.keys()])
        values = list(data_to_update.values()) + [recipe_id]
        sql = f"UPDATE Recipes SET {set_clause} WHERE RecipeId = ?"
        try:
            cursor.execute(sql, values)
            conn.commit()
        except Exception as e:
            print(f"שגיאה בעדכון: {e}")
        finally:
            conn.close()

def delete_recipe(id_value):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM Recipes WHERE RecipeId = ?"
        try:
            cursor.execute(sql, (id_value,))
            conn.commit()
        except Exception as e:
            print(f"שגיאה במחיקה: {e}")
        finally:
            conn.close()


def get_recipes_by_category(category: str):
    conn = get_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    # שימוש ב-trim למקרה שיש רווחים מיותרים ב-SQL
    cursor.execute(
        "SELECT * FROM Recipes WHERE LTRIM(RTRIM(Category)) = ?",
        (category.strip(),)
    )

    columns = [c[0] for c in cursor.description]
    recipes = [dict(zip(columns, row)) for row in cursor.fetchall()]

    conn.close()
    return recipes

