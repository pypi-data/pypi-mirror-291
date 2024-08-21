import requests


class TelegramLogger:
    _instance = None

    def __new__(cls, api_key=None, chat_id=None):
        if cls._instance is None:
            cls._instance = super(TelegramLogger, cls).__new__(cls)
            cls._instance.api_key = api_key
            cls._instance.chat_id = chat_id
            cls._instance.base_url = f"https://api.telegram.org/bot{cls._instance.api_key}/sendMessage"
        return cls._instance

    def capture_message(self, message: str):
        if self.api_key is None or self.chat_id is None:
            raise ValueError("TelegramLogger not initialized. Please call init_bibla() with API key and chat ID.")

        data = {
            "chat_id": self.chat_id,
            "text": message
        }
        response = requests.post(self.base_url, data=data)
        if response.status_code != 200:
            raise Exception(f"Failed to send message: {response.status_code} - {response.text}")
        return response.json()


def init_telegramm_bot(api_key: str, chat_id: str):
    """Инициализация логгера Telegram."""
    TelegramLogger(api_key, chat_id)


def capture_message(message: str):
    """Отправка сообщения в Telegram."""
    logger = TelegramLogger()
    logger.capture_message(message)
