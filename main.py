# -*- coding: utf-8 -*-
import requests, time, transliterate, gspread, re, sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("limits.db", check_same_thread=False)  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

sv_num = {"79513292383": "Екатерина Шишова",
          "79999696689": "Данила Грищенко",
          "79289556229": "Евгений Уваров"}
ids_regionals = {
    259111894: {
        "fio": "Веревкин Рег. Питер",
        "lim_day": 3000,
        "lim_mounth": 45000,
        "lim_on_1ak": 10000
    },
    844228517: {
        "fio": "Уваров Рег. ЮГ",
        "lim_day": 15000,
        "lim_mounth": 100000,
        "lim_on_1ak": 10000
    },
    557889049: {
        "fio": "Дормидонтова Рег. ПУС",
        "lim_day": 25000,
        "lim_mounth": 60000,
        "lim_on_1ak": 10000
    },
    529210954: {
        "fio": "Шишова Рег. Мск",
        "lim_day": 1000000,
        "lim_mounth": 8000000,
        "lim_on_1ak": 40000
    },
    331089681: {
        "fio": "Тимаховский Фед. Россия",
        "lim_day": 100000,
        "lim_mounth": 1000000,
        "lim_on_1ak": 100000
    },
    1896710241: {
        "fio": "Грищенко Д.С.",
        "lim_day": 999999,
        "lim_mounth": 999999,
        "lim_on_1ak": 999999
    },
    772977: {
        "fio": "Азаров Андрей",
        "lim_day": 50000,
        "lim_mounth": 300000,
        "lim_on_1ak": 300000
    },
    455179268: {
        "fio": "Кирилл Менеджер Краснодар",
        "lim_day": 20000,
        "lim_mounth": 50000,
        "lim_on_1ak": 5000
    },
    641069187: {
        "fio": "Амиран Амриев Только Завершение",
        "lim_day": 0,
        "lim_mounth": 0,
        "lim_on_1ak": 0
    },
    399360572: {
        "fio": "Максим Болдырев Только Завершение",
        "lim_day": 0,
        "lim_mounth": 0,
        "lim_on_1ak": 0
    },
    794164257: {
        "fio": "Влада Картавцева Только Завершение",
        "lim_day": 0,
        "lim_mounth": 0,
        "lim_on_1ak": 0
    },
    1028217588: {
        "fio": "Денис Зорин Только Завершение",
        "lim_day": 0,
        "lim_mounth": 0,
        "lim_on_1ak": 0
    },
    1337728541: {
        "fio": "Александр Яланджи Только Завершение",
        "lim_day": 5000,
        "lim_mounth": 55000,
        "lim_on_1ak": 10000
    },
    453054458: {
        "fio": "Марат Сейнсенбаев Только Завершение",
        "lim_day": 0,
        "lim_mounth": 0,
        "lim_on_1ak": 0
    },
    990925356: {
        "fio": "Игорь Смирнов ЮГ",
        "lim_day": 0,
        "lim_mounth": 0,
        "lim_on_1ak": 0
    }

}
headers_glob = {
    "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
    "TraceId": "JVCJ1FE9V8",
    "X-Vendor": "MURB",
    "X-Selected-Vendors": "MURB",
    "Authorization": "Bearer",
    "Accept-Language": "ru-RU",
    "Host": "service.urentbike.ru",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/3.12.6",
    "Content-Type": "application/json; charset=UTF-8",
    "Content-Length": "123"
}

data = {
    "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
    "TraceId": "60KPVNT24I",
    "X-Vendor": "NVU",
    "X-Selected-Vendors": "NVU",
    "Accept-Language": "ru-RU",
    "Host": "service.urentbike.ru",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/3.12.6",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content - Length": "659"
}

def in_google(name, row_g):
    time_now = time.strftime("%d.%m.%y %H:%M")
    row_res = [time_now]
    row_res += row_g
    row_res.append("-")
    row_res.append(time.strftime("%m"))
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key("1uSYDlnidZobK5ZsbizJQBEpWIWncfNuL9W3NAbsQV5g")
    worksheet = sh.worksheet(name)
    #   print(row_res)
    worksheet.append_row(row_res)


def find_customers(num):
    BASE_URL = 'https://service.urentbike.ru/customers/api/customers?filter={"text":"' + num + '"}&cPage=1&iOnPage=10'
    global headers_glob

    headers = {
        "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
        "TraceId": "BTOGUB8UZZ",
        "X-Vendor": "ADR",
        "X-Selected-Vendors": "ADR",
        "Authorization": "Bearer " + acc_token,
        "Accept-Language": "ru-RU",
        "Host": "service.urentbike.ru",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.6",
        "Content-Type": "application/json"
    }

    headers["Authorization"] = headers_glob["Authorization"]

    auth_response = requests.get(BASE_URL, headers=headers)
    if (auth_response.status_code == 401):
        refresh_token()
        auth_response = find_customers(num)
    elif (auth_response.status_code != 200):
        return auth_response
    return auth_response


def get_balanse(id):
    BASE_URL = 'https://service.urentbike.ru/payment/api/transactions/balances'
    global headers_glob
    headers = headers_glob
    data1 = '{"accountIds": ' + '["' + id + '"]}'
    auth_response1 = requests.post(BASE_URL, headers=headers, data=data1)

    if (auth_response1.status_code == 401):
        refresh_token()
        auth_response1 = get_balanse(id)
    elif (auth_response1.status_code != 200):
        print(auth_response1.json())
        return False
    return auth_response1


def send_money(money_count, id, desc):
    print("phone: " + str(id))
    BASE_URL1 = 'https://service.urentbike.ru/payment/api/Bonuses/enrollbyphone'
    global headers_glob
    headers = headers_glob
    data1 = '{"phone": "' + str(
        id) + '","value": {"value": ' + money_count + ',"culture": "ru-RU"},"description": "' + desc + '"}'
    auth_response1 = requests.post(BASE_URL1, headers=headers, data=data1)
    print(auth_response1.status_code)
    if (auth_response1.status_code == 401):
        refresh_token()
        auth_response1 = send_money(money_count, id, desc)
    elif (auth_response1.status_code != 200):
        return auth_response1
    return auth_response1


def withdraw_money_by_id(money, id):
    BASE_URL1 = 'https://service.urentbike.ru/payment/api/bonuses/withdraw'
    global headers_glob
    headers = headers_glob
    data1 = '{"accountIds": ["' + str(
        id) + '"],"value": {"value": ' + money + ',"culture": "ru-RU"},"description": "' + "Punishment" + '"}'
    auth_response1 = requests.post(BASE_URL1, headers=headers, data=data1)

    if (auth_response1.status_code == 401):
        refresh_token()
        auth_response1 = withdraw_money_by_id(money, id)
    elif (auth_response1.status_code != 200):
        return auth_response1
    return auth_response1


def get_data_from_base_by_limits(id_kto, ids_komu):
    time_now = datetime.today()
    mounth = int(time_now.strftime("%m"))
    day = int(time_now.strftime("%d"))
    cursor.execute("SELECT summa FROM m" + str(id_kto) + " WHERE date_mounth = '" + str(mounth) + "'")
    result_from_table = cursor.fetchall()
    summa_by_mounth = 0
    for i in result_from_table: summa_by_mounth += int(i[0])

    cursor.execute(
        "SELECT summa FROM m" + str(id_kto) + " WHERE date_mounth = '" + str(mounth) + "' AND date_day = '" + str(
            day) + "'")
    result_from_table = cursor.fetchall()
    summa_by_day = 0
    for i in result_from_table: summa_by_day += int(i[0])

    cursor.execute(
        "SELECT summa FROM m" + str(id_kto) + " WHERE date_mounth = '" + str(mounth) + "' AND komu = '" + str(
            ids_komu) + "'")
    result_from_table = cursor.fetchall()
    summa_by_user = 0
    for i in result_from_table: summa_by_user += int(i[0])
    return {"summa_by_user": summa_by_user,
            "summa_by_day": summa_by_day,
            "summa_by_mounth": summa_by_mounth}


def check_limits(id_kto, money, ids_komu):
    data = get_data_from_base_by_limits(id_kto, ids_komu)
    check_mounth = ids_regionals[id_kto]["lim_mounth"] >= (data["summa_by_mounth"] + int(money))
    check_day = ids_regionals[id_kto]["lim_day"] >= (data["summa_by_day"] + int(money))
    check_user = ids_regionals[id_kto]["lim_on_1ak"] >= (data["summa_by_user"] + int(money))

    control_check = check_day and check_user and check_mounth
    return (control_check)


def get_lim(id_kto, id_komu):
    dlina = 29
    text_result = "```\n" + ("#" * (dlina + 1)) + "\n"
    text_result += " " * int((dlina - 7) / 2) + "Остатки" + " " * int((dlina - 7) / 2) + "#\n" + dlina * " " + "#\n"
    data = get_data_from_base_by_limits(id_kto, id_komu)
    ost_day = ids_regionals[id_kto]["lim_day"] - data["summa_by_day"]
    ost_mounth = ids_regionals[id_kto]["lim_mounth"] - data["summa_by_mounth"]
    time_now = datetime.today()
    mounth = int(time_now.strftime("%m"))
    cursor.execute("SELECT komu FROM m" + str(id_kto) + " WHERE date_mounth = '" + str(mounth) + "'")
    result_from_base = cursor.fetchall()
    komu_ids_unik = []
    for i in result_from_base:
        if i[0] not in komu_ids_unik:
            komu_ids_unik.append(i[0])
    text_user_lim_ost = " "
    for i in komu_ids_unik:
        ost_by_user = ids_regionals[id_kto]["lim_on_1ak"] - get_data_from_base_by_limits(id_kto, i)["summa_by_user"]
        if ost_by_user < 1000:
            mes_user = str(i) + ": " + str(ost_by_user) + " б."
            text_user_lim_ost += "\n" + mes_user + (dlina - len(mes_user)) * " " + "#"
    mes_day = "Сегодня: " + str(ost_day) + " б."
    mes_mounth = "Меясц: " + str(ost_mounth) + " б."
    text_result += mes_day + " " * (dlina - len(mes_day)) + "#\n"
    text_result += mes_mounth + " " * (dlina - len(mes_mounth)) + "#\n"
    if text_user_lim_ost != " ":
        text_result += "К начислению менее 1к:" + " " * (dlina - 22) + "#"
        text_result += text_user_lim_ost
    text_result += "\n" + (dlina + 1) * "#" + "\n\n"
    text_result += "Вам доступно.\n"
    text_result += str(ids_regionals[id_kto]["lim_day"]) + " б. в день\n"
    text_result += str(ids_regionals[id_kto]["lim_mounth"]) + " б. в месяц\n"
    text_result += str(ids_regionals[id_kto]["lim_on_1ak"]) + " б. на один номер\n"
    text_result += "```"
    return text_result


def add_to_limits(id_kto, money, ids_komu):
    time_now = datetime.today()
    mounth = int(time_now.strftime("%m"))
    day = int(time_now.strftime("%d"))
    cursor.execute("INSERT INTO m" + str(id_kto) + " VALUES (?, ?, ?, ?)", (ids_komu, money, day, mounth))
    conn.commit()


def check_by_correct_number(find_tels):
    for i in range(len(find_tels)):
        print(find_tels[i])
        if find_tels[i][0] == "+": find_tels[i] = find_tels[i][2:]
        if find_tels[i][0] == "8" or find_tels[i][0] == "7": find_tels[i] = find_tels[i][1:len(find_tels[i])]

        if (not find_tels[i].isdigit()) or len(find_tels[i]) != 10:
            return {"result": False,
                    "text": "Ошибка с номером: " + find_tels[i] + "\nНикому не было начислено, надо отправить заново"
                    }

        find_tels[i] = "7" + find_tels[i]
    return {"result": True,
            "text": "Номера корректны."
            }


def bonus(massiv, message):
    massiv[0] = massiv[0].rstrip()
    find_tels = massiv[0].split(" ")
    print(find_tels)
    if not check_by_correct_number(find_tels)["result"]:
        bot.reply_to(message, check_by_correct_number(find_tels)["text"])
        return False

    if not massiv[1].isdigit() or massiv[1] == "0":
        mes = "Ошибка. Некорректна сумма начисления"
        bot.reply_to(message, mes)
        return False

    if not check_limits(message.from_user.id, massiv[1], 0):
        mes = "Начисление не проходит по лимитам.\n" + get_lim(message.from_user.id, 0)
        bot.reply_to(message, mes, parse_mode="Markdown")
        return False

    comment = massiv[2]
    for i in find_tels:
        try:
            if check_limits(message.from_user.id, massiv[1], i):
                result = send_money(massiv[1], i, transliterate.translit(comment, reversed=True)).status_code
                if int(result) == 200:
                    bot.reply_to(message, "Начислено: " + i)
                    add_to_limits(message.from_user.id, massiv[1], i)
                    if not ((message.from_user.id == 1896710241) and (massiv[2].lower() == "нет")):
                        in_google("Начисления 2023", [ids_regionals[message.from_user.id]["fio"], i, int(massiv[1]),
                                                      transliterate.translit(comment, reversed=True)])
                else:
                    bot.reply_to(message, "Ошибка по: " + i + "\nпроверьте корректность номера")
            else:
                bot.reply_to(message,
                             "Начисление на " + i + " не проходит по лимитам.\n" + get_lim(message.from_user.id, 0),
                             parse_mode="Markdown")
        except Exception as ex:
            print(str(ex))
            bot.reply_to(message, "Ошибка: " + i + "\n\n" + str(ex))

    #   except Exception as ex:
    #      bot.reply_to(message, "Произошла ошибка\n\n" + str(ex))
    #       return True


def end_rent(bike_id):
    BASE_URL1 = 'https://service.urentbike.ru/ordering/api/orders/forcedcloseforbike'
    global headers_glob
    headers = headers_glob
    data1 = '{"bikeIdentifier": ' + '"S.' + bike_id + '"}'
    try:
        auth_response1 = requests.post(BASE_URL1, headers=headers, data=data1)
    except Exception as ex:
        return "Ошибка"
    if (auth_response1.status_code == 401):
        refresh_token()
        return end_rent(bike_id)
    return str(auth_response1.json())


def read_on_file():
    f = open("otus.txt", encoding="utf-8")
    ref = f.readline()
    f.close()
    return ref


def write_on_file(name_file, ref):
    if name_file == "users.txt":
        o_mode = "a"
    else:
        o_mode = "w"
    file = open(name_file, o_mode, encoding="utf-8")
    file.write(ref)
    file.close()
    return True


def refresh_token():
    get = read_on_file()
    BASE_URL = 'https://service.urentbike.ru/identity/connect/token'
    data = {
        "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
        "TraceId": "60KPVNT24I",
        "X-Vendor": "NVU",
        "X-Selected-Vendors": "NVU",
        "Accept-Language": "ru-RU",
        "Host": "service.urentbike.ru",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.6",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content - Length": "659"
    }
    params = {
        "client_id": "mobile.technic",
        "client_secret": "4rrRqfWZLWr4DE1mOceAueBtiJDRwe6qwl5KrRz0DQU5jMhVMjl7nKovjPaFS4Te",
        "grant_type": "refresh_token",
        "scope": "identity.api%20bike.api%20maintenance.api%20location.api%20ordering.api%20ordering.scooter.api%20driver.scooter.tracker.navtelecom.api%20driver.bike.tracker.concox.api%20driver.bike.lock.offo.api%20driver.bike.lock.tomsk.api%20log.api%20payment.api%20customers.api%20driver.scooter.ninebot.api%20driver.scooter.teltonika.api%20driver.scooter.cityride.api%20driver.scooter.tracker.arusnavi.api%20driver.scooter.omni.api%20driver.scooter.voi.api%20offline_access",
        "refresh_token": get
    }
    auth_response = requests.post(BASE_URL, headers=data, data=params)
    global headers_glob
    headers_glob["Authorization"] = "Bearer " + auth_response.json()["access_token"]
    print(str(auth_response.json()["access_token"]))
    write_on_file("otus.txt", str(auth_response.json()["refresh_token"]))
    return auth_response


get = refresh_token().json()
acc_token = get["access_token"]
ref_token = get["refresh_token"]
print(acc_token)
import telebot

bot = telebot.TeleBot("1895259913:AAGjRcbLouTwVsOxifO1-VzKXenSd4RkEnw")


@bot.message_handler(commands=['minus'])
def start_message(message):
    bot.send_message(1896710241,
                     "```\n" + str(message.from_user.last_name) + "\n##########\n" + str(message.text) + "\n```",
                     parse_mode="Markdown")
    bot.reply_to(message, "1")
    data_mas = message.text.split(" ")
    if len(data_mas) != 3:
        bot.reply_to(message, "Error!")
        return True
    num = data_mas[1]
    summa = data_mas[2]
    bot.reply_to(message, "1.1")
    data_0 = find_customers(num).json()["entries"]
    bot.reply_to(message, "1.11")
    bot.reply_to(message, "1.13")
    if len(data_0) == 0:
        bot.reply_to(message, "1.14")
        bot.reply_to(message, "Error!")
        bot.reply_to(message, "1.11")
        return True
    bot.reply_to(message, "1.2")
    if str(data_mas[2]) != "0":
        bot.reply_to(message, "2")
        resilt = withdraw_money_by_id(data_mas[2], data_0[0]["accountId"])
        bot.reply_to(message, "3")
        resilt = resilt.status_code
        bot.reply_to(message, "4")
    data_1 = get_balanse(data_0[0]["accountId"]).json()["entries"][0]["bonus"]["value"]
    text = "Баланс: " + str(data_1) + " рублей"
    if resilt == 200: text = "Бонусы списаны.\n" + "Баланс: " + str(data_1) + " рублей"
    bot.reply_to(message, "5")
    bot.reply_to(message, text)


@bot.message_handler(commands=['start'])
def start_message(message):
    id_user = message.from_user.id
    if not id_user in ids_regionals.keys():
        bot.reply_to(message, "У вас нет доступа.")
        return False
    bot.reply_to(message, "*Авторизован: " + ids_regionals[id_user]["fio"] + "*", parse_mode="Markdown")
    bot.reply_to(message, get_lim(message.from_user.id, 0), parse_mode="Markdown")


@bot.message_handler(commands=['lim'])
def get_lim_mes(message):
    bot.send_message(1896710241,
                     "```\n" + str(message.from_user.last_name) + "\n##########\n" + str(message.text) + "\n```",
                     parse_mode="Markdown")
    bot.reply_to(message, get_lim(message.from_user.id, 0), parse_mode="Markdown")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе

    bot.send_message(1896710241, "```\n" + str(message.from_user.last_name) + "\n##########\n" + str(
        message.text) + "\n```", parse_mode="Markdown")

    id_user = message.from_user.id

    if not id_user in ids_regionals.keys():
        bot.reply_to(message, "У вас нет доступа.")
        return False

    massiv = message.text.split("\n")
    if len(massiv) == 3:
        bonus(massiv, message)
    elif len(massiv) == 1 and massiv[0].isdigit() and len(massiv[0]) < 7:
        result = end_rent(message.text)
        bot.reply_to(message, result)
        in_google("Завершения", [ids_regionals[message.from_user.id]["fio"], message.text, result])
    else:
        bot.reply_to(message, "ошибка")
        return True


# for i in list(ids_regionals.keys()):bot.send_message(i, "*Всем привет! Бот работает заново :)*", parse_mode="Markdown")
# bot.send_message(529210954, "*)))*", parse_mode="Markdown")
# bot.send_message(1896710241, "*Можно оплачивать офис!!!!!!!*", parse_mode="Markdown")

if __name__ == '__main__':
    bot.polling(none_stop=True)