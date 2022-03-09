# DominiGamesTestTasks
1.Рекурсивно привести папки и файлы к нижнему регистру. Перевести все файлы в utf-8.

Кроме того, рекомендуется самостоятельно тестировать код перед отправкой, а также при написании следовать стандарту PEP 8.
```
import sys
import os


def cur_file_dir():
    # Получить текущий путь к файлу
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def rename(path):
    file_list = os.listdir(path)
    # print(file_list)
    for file in file_list:
        # print(file)
        old_dir = os.path.join(path, file)
        filename = os.path.splitext(file)[0]
        # print(filename)
        filetype = os.path.splitext(file)[1]
        # print(filetype)
        new_name = filename.replace(filename, filename.lower())
        new_dir = os.path.join(path, new_name + filetype)
        os.rename(old_dir, new_dir)
        if os.path.isdir(new_dir):
            rename(new_dir)


if __name__ == "__main__":
    path = cur_file_dir()
    rename(path)
   ```
2.Даны 3 документа: Excel документ (или желательно использовать Google Sheet), Info.plist и DominiIAP.xml, в которых необходимо проверить поля на валидность из Excel документа. В случае несоответствия выводить в консоль ошибку и правильный ключ. Количество ключей в Excel таблице может изменяться.
```
from xml.dom import minidom
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

plist_UniversalF2P = {}
purchase = {}


def getExcel():
    CREDENTIALS_FILE = 'credentials.json'
    spreadsheet_id = '1m9uq587LomH2L8Wid2Ym4K1BFz1azbHi4BT6tAxbEb8'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API
    counter1 = 2
    while True:
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A' + str(counter1) + ':' + 'A' + str(counter1),
            majorDimension='ROWS'
        ).execute()
        resultKey = values.get('values', [])
        if len(resultKey) == 0:
            break
        else:
            resultKey = resultKey[0][0]

        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='B' + str(counter1) + ':' + 'B' + str(counter1),
            majorDimension='ROWS'
        ).execute()
        resultValue = values.get('values', [])
        resultValue = resultValue[0][0]
        counter1 += 1
        plist_UniversalF2P[resultKey] = resultValue
        # print(plist_UniversalF2P)
    counter2 = 2
    while True:
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='C' + str(counter2) + ':' + 'C' + str(counter2),
            majorDimension='ROWS'
        ).execute()
        resultKey = values.get('values', [])
        if len(resultKey) == 0:
            break
        else:
            resultKey = resultKey[0][0]

        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='D' + str(counter2) + ':' + 'D' + str(counter2),
            majorDimension='ROWS'
        ).execute()
        resultValue = values.get('values', [])
        resultValue = resultValue[0][0]
        counter2 += 1
        purchase[resultKey] = resultValue
        # print(purchase)


def getMyXMl(file):
    dom = minidom.parse(file)
    dom.normalize()
    # print(dom)
    elements = dom.getElementsByTagName('item')
    current_dict = {}

    for node in elements:
        # print(node)
        for child in node.childNodes:
            # print (child)
            if child.nodeType == 1:
                if child.tagName == 'ProductID':
                    if child.firstChild.nodeType == 3:
                        ProductID = child.firstChild.data
                if child.tagName == 'analytics_event_name' and child.firstChild.data != '':
                    if child.firstChild.nodeType == 3:
                        analytics_event_name = child.firstChild.data
                elif child.tagName == 'store_desc':
                    if child.firstChild.nodeType == 3:
                        analytics_event_name = child.firstChild.data

        current_dict[ProductID] = analytics_event_name
    return current_dict


def get_plist(file):
    dom = minidom.parse(file)
    dom.normalize()
    # print(dom)
    elements = dom.getElementsByTagName('dict')
    # print(elements)
    current_dict = {}
    for node in elements:
        # print(node)
        for child in node.childNodes:
            # print (child)
            if child.nodeType == 1:
                if child.tagName == 'key':
                    if child.firstChild.nodeType == 3:
                        key = child.firstChild.data
                        # print(key)
                if child.tagName == 'string':
                    if child.firstChild.nodeType == 3:
                        value = child.firstChild.data
                        # print(value)
                        current_dict[key] = value
        current_dict[key] = value
    return current_dict


if __name__ == '__main__':
    getExcel()
    xml_data = getMyXMl('DominiIAP.xml')
    plist = get_plist('info.plist')
    # print(xml_data)
    # print((plist))
    # print(plist_UniversalF2P)
    # print(purchase)
    for i in purchase:
        if i in xml_data:
            if purchase[i] == xml_data[i]:
                print("Значания совпадают:" +
                      i + ': ' + purchase[i] + " из таблицы Google sheets и " +
                      i + ': ' + xml_data[i] + ' из файла DominiIAP.xml')
            else:
                raise ValueError \
                    ("Значания не совпадают:" +
                     i + ': ' + purchase[i] + " из таблицы Google sheets и " +
                     i + ': ' + xml_data[i] + ' из файла DominiIAP.xml')

    for i in plist_UniversalF2P:
        if i in plist:
            if plist_UniversalF2P[i] == plist[i]:
                print("Значания совпадают:" +
                      i + ': ' + plist_UniversalF2P[i] + " из таблицы Google sheets и " +
                      i + ': ' + plist[i] + ' из файла info.plist')
            else:
                raise ValueError \
                    ("Значания не совпадают:" +
                     i + ': ' + plist_UniversalF2P[i] + " из таблицы Google sheets и " +
                     i + ': ' + plist[i] + ' из файла info.plist')
```
