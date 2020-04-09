import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from TelegramEasy.Bot_token import google_sheet_id


def do_cargo_google(company):
    cred_file = '/Users/rob/Documents/Code/my_projects/google_sheets/Tracing-adf1c6e6f518.json'
    sheet_id = google_sheet_id
    # Подключаем апи на гугл драйв и таблицы
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Qty of row in file
    row_n = service.spreadsheets().values().get(spreadsheetId=sheet_id, range='A1:A300',
                                                majorDimension='COLUMNS').execute()
    row_qty_ch = len(row_n['values'][0])
    now = datetime.datetime.now().date()

    lst_final = []
    company_lst = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'China!E1:E{row_qty_ch}',
                                                      majorDimension='COLUMNS').execute()
    dostavka = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'China!W1:W{row_qty_ch}',
                                                   majorDimension='COLUMNS').execute()
    num_B = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'China!B1:B{row_qty_ch}',
                                                majorDimension='COLUMNS').execute()
    km_R = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'China!R1:R{row_qty_ch}',
                                               majorDimension='COLUMNS').execute()
    port_O = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'China!O1:O{row_qty_ch}',
                                                 majorDimension='COLUMNS').execute()
    DO_V = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'China!V1:V{row_qty_ch}',
                                               majorDimension='COLUMNS').execute()
    dep_N = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'China!N1:N{row_qty_ch}',
                                                majorDimension='COLUMNS').execute()
    red_M = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'China!M1:M{row_qty_ch}',
                                                majorDimension='COLUMNS').execute()
    svh_Q = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'China!Q1:Q{row_qty_ch}',
                                                majorDimension='COLUMNS').execute()
    wh_S = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'China!S1:S{row_qty_ch}',
                                                majorDimension='COLUMNS').execute()

    for el in range(1, row_qty_ch + 1):
        if wh_S['values'][0][el - 1] != '0' and company_lst['values'][0][el - 1] == company and dostavka['values'][0][el - 1] != 'закрыта':
            lst_final.append(f'{num_B["values"][0][el - 1]} -- Доставка назначена на {wh_S["values"][0][el - 1]}')
        else:
            if km_R['values'][0][el - 1] != '0' and company_lst['values'][0][el - 1] == company and dostavka['values'][0][el - 1] != 'закрыта':
                if svh_Q["values"][0][el - 1] == '0':
                    lst_final.append(f'{num_B["values"][0][el - 1]} -- {km_R["values"][0][el - 1]}')
                else:
                    date1 = datetime.datetime.strptime(svh_Q["values"][0][el - 1], '%d.%m.%Y').date()
                    if (date1 - now).days <= 0:
                        lst_final.append(f'{num_B["values"][0][el - 1]} -- {km_R["values"][0][el - 1]}')
                    elif (date1 - now).days > 0:
                        lst_final.append(f'{num_B["values"][0][el - 1]} -- {km_R["values"][0][el - 1]} -- приход {svh_Q["values"][0][el - 1]}')

            elif km_R['values'][0][el - 1] == '0' and company_lst['values'][0][el - 1] == company and \
                dostavka['values'][0][el - 1] != 'закрыта' \
                and port_O['values'][0][el - 1] != '0':
                date = datetime.datetime.strptime(port_O["values"][0][el - 1], '%d.%m.%Y').date()
                if (date - now).days > 0:
                    lst_final.append(f'{num_B["values"][0][el - 1]} -- в порт через {(date - now).days} день')
                elif (date - now).days <= 0:
                    lst_final.append(f'{num_B["values"][0][el - 1]} -- {DO_V["values"][0][el - 1]}')

            elif km_R['values'][0][el - 1] == '0' and company_lst['values'][0][el - 1] == company and \
                dostavka['values'][0][el - 1] != 'закрыта' \
                and port_O['values'][0][el - 1] == '0' and dep_N['values'][0][el - 1] == '0' and red_M['values'][0][el - 1] != '0':
                lst_final.append(f'{num_B["values"][0][el - 1]} -- Дата выхода судна еще не незначена!')

    # Europe!!!
    row_n_e = service.spreadsheets().values().get(spreadsheetId=sheet_id, range='Europe!A1:A300',
                                                  majorDimension='COLUMNS').execute()
    row_qty_e = len(row_n_e['values'][0])
    company_lst_e = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'Europe!E1:E{row_qty_e}',
                                                        majorDimension='COLUMNS').execute()
    ar_N = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'Europe!N1:N{row_qty_e}',
                                               majorDimension='COLUMNS').execute()
    dost_e_Q = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'Europe!Q1:Q{row_qty_e}',
                                                   majorDimension='COLUMNS').execute()
    post_e_B = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'Europe!B1:B{row_qty_e}',
                                                   majorDimension='COLUMNS').execute()
    SVH_e_M = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'Europe!M1:M{row_qty_e}',
                                                  majorDimension='COLUMNS').execute()
    dep_e_K = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'Europe!K1:K{row_qty_e}',
                                                  majorDimension='COLUMNS').execute()

    for el in range(1, row_qty_e + 1):
        if ar_N['values'][0][el - 1] != '0' and dost_e_Q['values'][0][el - 1] != 'закрыта' and \
                company_lst_e['values'][0][el - 1] == company:
            lst_final.append(f'{post_e_B["values"][0][el - 1]} - Выгрузка назначена на {ar_N["values"][0][el - 1]}')

        elif ar_N['values'][0][el - 1] == '0' and dost_e_Q['values'][0][el - 1] != 'закрыта' \
                and company_lst_e['values'][0][el - 1] == company and SVH_e_M['values'][0][el - 1] != '0':
            date_e = datetime.datetime.strptime(SVH_e_M["values"][0][el - 1], '%d.%m.%Y').date()
            if (date_e - now).days > 0:
                lst_final.append(f'{post_e_B["values"][0][el - 1]} - приход на СВХ через {(date_e - now).days} дня')

            elif (date_e - now).days <= 0:
                lst_final.append(f'{post_e_B["values"][0][el - 1]} - подача ДТ')

        elif ar_N['values'][0][el - 1] == '0' and dost_e_Q['values'][0][el - 1] != 'закрыта' \
                and company_lst_e['values'][0][el - 1] == company and SVH_e_M['values'][0][el - 1] == '0' and \
                dep_e_K['values'][0][el - 1] == '0':
            lst_final.append(f'{post_e_B["values"][0][el - 1]} - Дата забора груза согласовывается!')

    return '\n'.join(lst_final)
