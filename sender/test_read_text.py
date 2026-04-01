from datetime import datetime

# Получаем текущую дату
current_date = datetime.now()
day = current_date.day
month = current_date.month
year = current_date.year

# Формируем путь (ВАЖНО: без / в начале)
message_path = f"txt/{year}/{month}/{day}.txt"

print(f"Reading file: {message_path}")

try:
    with open(message_path, 'r', encoding='utf-8') as file:
        messageText = file.read()

    print("\n=== FILE CONTENT ===")
    print(messageText)

except FileNotFoundError:
    print("❌ File not found")
except Exception as e:
    print(f"❌ Error: {e}")
