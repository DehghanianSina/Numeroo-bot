import re
import os
import phonenumbers
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()

# Get bot token from environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN not found in .env file")
    exit(1)

def normalize_phone_number(phone: str) -> str:
    """Normalize phone number by removing spaces and converting Persian digits to English."""
    # Convert Persian digits to English
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    translation_table = str.maketrans(persian_digits, english_digits)
    phone = phone.translate(translation_table)
    
    # Remove all non-digit characters except '+'
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Handle Iranian numbers
    if phone.startswith('98'):
        phone = phone[2:]
    elif phone.startswith('+98'):
        phone = phone[3:]
    elif phone.startswith('0098'):
        phone = phone[4:]
    elif phone.startswith('0'):
        phone = '98' + phone[1:]
    
    # If the number starts with +, keep it
    if phone.startswith('+'):
        return phone[1:]  # Remove the + as it will be added in the link
    
    return phone

def get_country_info(phone_number: str) -> tuple:
    """Get country information from phone number"""
    try:
        # Parse phone number
        parsed_number = phonenumbers.parse(phone_number)
        country_code = phonenumbers.region_code_for_number(parsed_number)
        
        # Get country name
        country_names = {
            "AF": "Afghanistan",
            "AL": "Albania",
            "DZ": "Algeria",
            "AD": "Andorra",
            "AO": "Angola",
            "AG": "Antigua and Barbuda",
            "AR": "Argentina",
            "AM": "Armenia",
            "AU": "Australia",
            "AT": "Austria",
            "AZ": "Azerbaijan",
            "BS": "Bahamas",
            "BH": "Bahrain",
            "BD": "Bangladesh",
            "BB": "Barbados",
            "BY": "Belarus",
            "BE": "Belgium",
            "BZ": "Belize",
            "BJ": "Benin",
            "BT": "Bhutan",
            "BO": "Bolivia",
            "BA": "Bosnia and Herzegovina",
            "BW": "Botswana",
            "BR": "Brazil",
            "BN": "Brunei",
            "BG": "Bulgaria",
            "BF": "Burkina Faso",
            "BI": "Burundi",
            "CV": "Cabo Verde",
            "KH": "Cambodia",
            "CM": "Cameroon",
            "CA": "Canada",
            "CF": "Central African Republic",
            "TD": "Chad",
            "CL": "Chile",
            "CN": "China",
            "CO": "Colombia",
            "KM": "Comoros",
            "CG": "Congo",
            "CD": "Congo (Democratic Republic)",
            "CR": "Costa Rica",
            "CI": "Côte d'Ivoire",
            "HR": "Croatia",
            "CU": "Cuba",
            "CY": "Cyprus",
            "CZ": "Czech Republic",
            "DK": "Denmark",
            "DJ": "Djibouti",
            "DM": "Dominica",
            "DO": "Dominican Republic",
            "EC": "Ecuador",
            "EG": "Egypt",
            "SV": "El Salvador",
            "GQ": "Equatorial Guinea",
            "ER": "Eritrea",
            "EE": "Estonia",
            "SZ": "Eswatini",
            "ET": "Ethiopia",
            "FJ": "Fiji",
            "FI": "Finland",
            "FR": "France",
            "GA": "Gabon",
            "GM": "Gambia",
            "GE": "Georgia",
            "DE": "Germany",
            "GH": "Ghana",
            "GR": "Greece",
            "GD": "Grenada",
            "GT": "Guatemala",
            "GN": "Guinea",
            "GW": "Guinea-Bissau",
            "GY": "Guyana",
            "HT": "Haiti",
            "HN": "Honduras",
            "HU": "Hungary",
            "IS": "Iceland",
            "IN": "India",
            "ID": "Indonesia",
            "IR": "Iran",
            "IQ": "Iraq",
            "IE": "Ireland",
            "IL": "Israel",
            "IT": "Italy",
            "JM": "Jamaica",
            "JP": "Japan",
            "JO": "Jordan",
            "KZ": "Kazakhstan",
            "KE": "Kenya",
            "KI": "Kiribati",
            "KP": "Korea (North)",
            "KR": "Korea (South)",
            "KW": "Kuwait",
            "KG": "Kyrgyzstan",
            "LA": "Laos",
            "LV": "Latvia",
            "LB": "Lebanon",
            "LS": "Lesotho",
            "LR": "Liberia",
            "LY": "Libya",
            "LI": "Liechtenstein",
            "LT": "Lithuania",
            "LU": "Luxembourg",
            "MG": "Madagascar",
            "MW": "Malawi",
            "MY": "Malaysia",
            "MV": "Maldives",
            "ML": "Mali",
            "MT": "Malta",
            "MH": "Marshall Islands",
            "MR": "Mauritania",
            "MU": "Mauritius",
            "MX": "Mexico",
            "FM": "Micronesia",
            "MD": "Moldova",
            "MC": "Monaco",
            "MN": "Mongolia",
            "ME": "Montenegro",
            "MA": "Morocco",
            "MZ": "Mozambique",
            "MM": "Myanmar",
            "NA": "Namibia",
            "NR": "Nauru",
            "NP": "Nepal",
            "NL": "Netherlands",
            "NZ": "New Zealand",
            "NI": "Nicaragua",
            "NE": "Niger",
            "NG": "Nigeria",
            "MK": "North Macedonia",
            "NO": "Norway",
            "OM": "Oman",
            "PK": "Pakistan",
            "PW": "Palau",
            "PA": "Panama",
            "PG": "Papua New Guinea",
            "PY": "Paraguay",
            "PE": "Peru",
            "PH": "Philippines",
            "PL": "Poland",
            "PT": "Portugal",
            "QA": "Qatar",
            "RO": "Romania",
            "RU": "Russia",
            "RW": "Rwanda",
            "KN": "Saint Kitts and Nevis",
            "LC": "Saint Lucia",
            "VC": "Saint Vincent and the Grenadines",
            "WS": "Samoa",
            "SM": "San Marino",
            "ST": "Sao Tome and Principe",
            "SA": "Saudi Arabia",
            "SN": "Senegal",
            "RS": "Serbia",
            "SC": "Seychelles",
            "SL": "Sierra Leone",
            "SG": "Singapore",
            "SK": "Slovakia",
            "SI": "Slovenia",
            "SB": "Solomon Islands",
            "SO": "Somalia",
            "ZA": "South Africa",
            "SS": "South Sudan",
            "ES": "Spain",
            "LK": "Sri Lanka",
            "SD": "Sudan",
            "SR": "Suriname",
            "SE": "Sweden",
            "CH": "Switzerland",
            "SY": "Syria",
            "TJ": "Tajikistan",
            "TZ": "Tanzania",
            "TH": "Thailand",
            "TL": "Timor-Leste",
            "TG": "Togo",
            "TO": "Tonga",
            "TT": "Trinidad and Tobago",
            "TN": "Tunisia",
            "TR": "Turkey",
            "TM": "Turkmenistan",
            "TV": "Tuvalu",
            "UG": "Uganda",
            "UA": "Ukraine",
            "AE": "United Arab Emirates",
            "GB": "United Kingdom",
            "US": "United States",
            "UY": "Uruguay",
            "UZ": "Uzbekistan",
            "VU": "Vanuatu",
            "VA": "Vatican City",
            "VE": "Venezuela",
            "VN": "Vietnam",
            "YE": "Yemen",
            "ZM": "Zambia",
            "ZW": "Zimbabwe"
        }
        
        country_name = country_names.get(country_code, country_code)
        
        # Generate flag emoji
        flag = ''.join(chr(ord(c) + 127397) for c in country_code)
        
        return flag, f"{country_name} ({country_code})"
    except:
        return None, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = (
        "👋 به Numeroo خوش آمدید!\n\n"
        "من می‌توانم لینک تلگرام و واتساپ شماره موبایل شما را ایجاد کنم.\n\n"
        "📱 لطفاً شماره موبایل خود را به یکی از فرمت‌های زیر ارسال کنید:\n"
        "• ۰۹۱۲۱۲۳۴۵۶۷\n"
        "• ۹۸۹۱۲۱۲۳۴۵۶۷\n"
        "• +۹۸۹۱۲۱۲۳۴۵۶۷\n"
        "• ۰۰۹۸۹۱۲۱۲۳۴۵۶۷\n\n"
        "🌍 همچنین می‌توانید شماره‌های بین‌المللی را هم همراه با کد کشور وارد کنید.\n\n"
        "من کشور مربوط به شماره را شناسایی می‌کنم و لینک‌های مربوطه را برای شما ارسال می‌کنم."
    )
    await update.message.reply_text(welcome_message)

async def handle_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the phone number input and generate Telegram link."""
    phone = update.message.text
    normalized_phone = normalize_phone_number(phone)
    
    if len(normalized_phone) < 10:
        await update.message.reply_text('شماره موبایل وارد شده نامعتبر است.')
        return
    
    # Get country information
    flag_emoji, country_name = get_country_info(f"+{normalized_phone}")
    
    if not country_name:
        await update.message.reply_text('کشور مربوط به این شماره موبایل شناسایی نشد.')
        return
    
    telegram_link = f't.me/+{normalized_phone}'
    whatsapp_link = f'wa.me/{normalized_phone}'
    await update.message.reply_text(
        f'{flag_emoji} {country_name}\n'
        f'{telegram_link}\n'
        f'{whatsapp_link}',
        disable_web_page_preview=True
    )

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone_number))

    # Start the Bot
    print("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()