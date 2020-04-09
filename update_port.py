import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from excel.web_serch import find_DO1


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
cred_file = '/Users/rob/Documents/Code/my_projects/google_sheets/Tracing-adf1c6e6f518.json'

creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)

client = gspread.authorize(creds)

sheet = client.open('Easy_Tracing').sheet1
# Кол-во активных строк:
row_qty = len(sheet.col_values(1))

now = datetime.datetime.now()

lst_to_check = []
for el in range(2, len(sheet.col_values(15))):
    if sheet.cell(el, 15).value != '0':
        if (now - datetime.timedelta(days=4)).date() < datetime.datetime.strptime(sheet.cell(el, 15).value, '%d.%m.%Y').date() < (now + datetime.timedelta(days=2)).date():
            if "ДО1" not in sheet.cell(el, 22).value:
                lst_to_check.append(el)

print(lst_to_check)

for el in lst_to_check:
    if sheet.cell(el, 8).value != '0':
        sheet.update(f'V{el}', f'{find_DO1(sheet.cell(el, 8).value)}')
    else:
        sheet.update(f'V{el}', 'Внесите номер контейнера!')


