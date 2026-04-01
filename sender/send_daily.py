import os
import time
from datetime import datetime
from pathlib import Path

import requests


def is_success_response(response):
    try:
        data = response.json()
    except Exception:
        return False, None

    # Для GreenAPI одного status_code == 200 недостаточно
    # Считаем успехом наличие idMessage
    return response.status_code == 200 and "idMessage" in data, data


def send_whatsapp_message(message_text, image_file_binary, max_attempts):
    api_url = "https://7107.api.greenapi.com"
    media_url = "https://7107.media.greenapi.com"

    id_instance = os.environ["GREEN_API_ID_INSTANCE"]
    api_token_instance = os.environ["GREEN_API_TOKEN_INSTANCE"]
    chat_id = os.environ["GREEN_API_CHAT_ID"]

    def send_image():
        for attempt in range(max_attempts):
            try:
                url = f"{media_url}/waInstance{id_instance}/sendFileByUpload/{api_token_instance}"
                payload = {
                    "chatId": chat_id,
                    "caption": ""
                }
                files = [
                    ("file", ("daily-reading.jpg", image_file_binary, "image/jpeg"))
                ]

                response = requests.post(url, data=payload, files=files, timeout=60)

                ok, data = is_success_response(response)
                if ok:
                    print(f"WhatsApp sendFileByUpload success: {data}")
                    return True
                else:
                    print(f"WhatsApp sendFileByUpload error: {response.status_code} {response.text}")
                    if attempt < max_attempts - 1:
                        wait_time = 2 ** attempt
                        print(f"Retrying image after {wait_time} seconds...")
                        time.sleep(wait_time)

            except Exception as e:
                print(f"WhatsApp sendFileByUpload exception: {e}")
                if attempt < max_attempts - 1:
                    wait_time = 2 ** attempt
                    print(f"Retrying image after {wait_time} seconds...")
                    time.sleep(wait_time)

        return False

    def send_text():
        for attempt in range(max_attempts):
            try:
                headers = {"Content-Type": "application/json"}
                url = f"{api_url}/waInstance{id_instance}/sendMessage/{api_token_instance}"
                data = {
                    "chatId": chat_id,
                    "message": message_text
                }

                response = requests.post(url, headers=headers, json=data, timeout=60)

                ok, data = is_success_response(response)
                if ok:
                    print(f"WhatsApp sendMessage success: {data}")
                    return True
                else:
                    print(f"WhatsApp sendMessage error: {response.status_code} {response.text}")
                    if attempt < max_attempts - 1:
                        wait_time = 2 ** attempt
                        print(f"Retrying text after {wait_time} seconds...")
                        time.sleep(wait_time)

            except Exception as e:
                print(f"WhatsApp sendMessage exception: {e}")
                if attempt < max_attempts - 1:
                    wait_time = 2 ** attempt
                    print(f"Retrying text after {wait_time} seconds...")
                    time.sleep(wait_time)

        return False

    image_sent = send_image()
    print()
    text_sent = send_text()

    return image_sent and text_sent


def main():
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year

    photo_path = Path(f"img/{year}/{month}/{day}.jpg")
    message_path = Path(f"txt/{year}/{month}/{day}.txt")

    print(f"Image path: {photo_path}")
    print(f"Text path: {message_path}")

    if not photo_path.exists():
        raise FileNotFoundError(f"Image file not found: {photo_path}")

    if not message_path.exists():
        raise FileNotFoundError(f"Text file not found: {message_path}")

    with open(photo_path, "rb") as file:
        image_file_binary = file.read()

    with open(message_path, "r", encoding="utf-8") as file:
        message_text = file.read()

    whatsapp_max_attempts = 3

    success = send_whatsapp_message(
        message_text=message_text,
        image_file_binary=image_file_binary,
        max_attempts=whatsapp_max_attempts
    )

    print()
    print(f"Done. Success={success}")

    if not success:
        raise RuntimeError("WhatsApp sending failed")


if __name__ == "__main__":
    main()











