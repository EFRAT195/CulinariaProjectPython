def welcome_message(name):
    """פונקציה שמחזירה ברכת שלום פשוטה"""
    return f"Hello {name}, welcome to the project!"


def calculate_average(numbers):
    """פונקציה לחישוב ממוצע של רשימת מספרים"""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def get_file_info():
    """פונקציה שמחזירה פרטים בסיסיים על המערכת"""
    import platform
    return {
        "system": platform.system(),
        "version": platform.version(),
        "language": "Python"
    }


if __name__ == "__main__":
    # הדגמה של הקוד
    print(welcome_message("Developer"))

    sample_data = [10, 20, 30, 40, 50]
    avg = calculate_average(sample_data)
    print(f"The average of the list is: {avg}")

    info = get_file_info()
    print(f"Running on {info['system']} using {info['language']}")