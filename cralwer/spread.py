import gspread
import ujson
from cralwer.config import SPREADSHEET_URL
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
SHEET = "시트1"
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", SCOPE
)
gc = gspread.authorize(credentials)
doc = gc.open_by_url(SPREADSHEET_URL)
worksheet = doc.worksheet(SHEET)
