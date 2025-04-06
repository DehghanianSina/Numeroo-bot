# Numeroo-bot 🤖

A smart Telegram bot that generates Telegram and WhatsApp links from phone numbers. 
Detects country information and displays country flag emoji.

## Features

- 🌍 Supports international phone numbers
- 🏳️ Detects country and displays flag
- 🔗 Generates Telegram and WhatsApp links
- 📱 Handles various phone number formats
- 🇮🇷 Supports Persian digits
- ✨ Disables link previews for cleaner messages

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Numeroo-bot.git
cd Numeroo-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp env.example .env
```

5. Edit `.env` and add your Telegram bot token:
```bash
cp .env.example .env
```
سپس توکن بات را در فایل `.env` قرار دهید.

6. بات را اجرا کنید:
```bash
python bot.py
```

## استفاده
1. بات را در تلگرام پیدا کنید و روی دکمه Start کلیک کنید.
2. شماره موبایل خود را به هر فرمتی که می‌خواهید وارد کنید.
3. بات لینک تلگرام مربوط به شماره شما را ارسال خواهد کرد. 

## Example Output

```
🇮🇷 Iran (IR)
t.me/+989121234567
wa.me/989121234567
```

## Technologies Used

- Python 3.11+
- python-telegram-bot
- phonenumbers
- python-dotenv

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 