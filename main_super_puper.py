# -*- coding: utf-8 -*-
import requests, csv, time, transliterate, gspread, pyshorteners, re

sv_num = {"79513292383": "Екатерина Шишова",
          "79775193376": "Глеб Пилат",
          "79775532003": "Александр Маричук",
          "79999696689": "Данила Грищенко",
          "79299217525": "Дмитрий Попов",
          "79881603809": "Анастасия Васильева",
          "79289556229": "Евгений Уваров"}

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

error_str = "Неправильно введены данные.\n\nФормат:\nТелефон\nСумма\nКомменатрий\n\nПример:\n9999696689\n500\nПромо"
error_str1 = "Ошибка.\nНеправильно указана сумма."
error_str2 = "Ошибка.\nНеправильно указан номер телефона."
error_str3 = "Ошибка.\nСумма не может быть нулевой или превышать 5000 рублей."


def write_data(filename, row):
    exampleFile = open(filename, 'a', encoding='UTF-8', newline='')
    exampleWriter = csv.writer(exampleFile, delimiter=';')
    exampleWriter.writerow(row)
    exampleFile.close()


def read_data(phone):
    with open("acc_id.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] == phone:
                return [row[1], row[2]]
        return "no"


def in_google(row_g):
    write_data("history_func.csv", ["Начал фун запись в гугл"])
    time_now = time.strftime("%d.%m.%y %H:%M")
    row_g[4] = time_now
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key("1uSYDlnidZobK5ZsbizJQBEpWIWncfNuL9W3NAbsQV5g")
    worksheet = sh.worksheet("Action")
    worksheet.resize(1000)
    worksheet.append_row(row_g)


def write_on_file(name_file, ref):
    if name_file == "users.txt":
        o_mode = "a"
    else:
        o_mode = "w"
    file = open(name_file, o_mode, encoding="utf-8")
    file.write(ref)
    file.close()
    return True


def read_on_file():
    f = open("otus.txt", encoding="utf-8")
    ref = f.readline()
    f.close()
    return ref


def get_active(cpage):
    write_data("history_func.csv", ["Начал функцию запроса активных"])
    BASE_URL = 'https://service.urentbike.ru/ordering/api/activity/all?cPage='+str(cpage)+'&iOnPage=1000'
    headers = {
        "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
        "TraceId": "ADBTU8YEGU",
        "X-Vendor": "ADR",
        "X-Selected-Vendors": "MOCHM,MOKRG,MOLBI,MOODV,MOU,MURB,VDNH",
        "Authorization": "Bearer " + acc_token,
        "Accept-Language": "ru-RU",
        "Host": "service.urentbike.ru",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.6",
    }

    headers["Authorization"] = headers_glob["Authorization"]

    auth_response = requests.get(BASE_URL, headers=headers)
    if (auth_response.status_code == 401):
        refresh_token()
        auth_response = get_active(cpage)
    elif (auth_response.status_code != 200):
        return False
    return auth_response


def get_balanse_req(id):
    write_data("history_func.csv", ["start get_balanse_req"])
    BASE_URL = 'https://service.urentbike.ru/payment/api/transactions/balances'
    global headers_glob
    headers = headers_glob
    data1 = '{"accountIds": ' + '["' + id + '"]}'
    auth_response1 = requests.post(BASE_URL, headers=headers, data=data1)

    if (auth_response1.status_code == 401):
        refresh_token()
        auth_response1 = get_balanse_req(id)
    elif (auth_response1.status_code != 200):
        return False
    return auth_response1


def get_balanse(id):
    write_data("history_func.csv", ["start get_balanse"])
    auth_response1 = get_balanse_req(id).json()
    bonus = auth_response1['entries'][0]['bonus']['valueFormatted']
    promocodes = ""
    for i in auth_response1['entries'][0]["promoCodes"]:
        promocodes += i["code"] + " " + i["bonus"]["valueFormatted"] + "\n"
    return [bonus, promocodes]


def get_zones(num):
    write_data("history_func.csv", ["start get_zones"])
    BASE_URL = 'https://customers.service.urentbike.ru/api/customers?filter={"text":"' + num + '"}&cPage=1&iOnPage=10'
    global headers_glob

    headers = {
        "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
        "TraceId": "60KPVNT24I",
        "X-Vendor": "ADR",
        "X-Selected-Vendors": "ADR",
        "Authorization": "Bearer " + acc_token,
        "Accept-Language": "ru-RU",
        "Host": "customers.service.urentbike.ru",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.6",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    headers["Authorization"] = headers_glob["Authorization"]

    auth_response = requests.get(BASE_URL, headers=headers)
    if (auth_response.status_code == 401):
        refresh_token()
        auth_response = get_zones(num)
    elif (auth_response.status_code != 200):
        return False
    return auth_response


def lock_unlock(phone, type_make):
    BASE_URL = 'https://service.urentbike.ru/identity/api/users' + type_make
    headers = {
        "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
        "TraceId": "60KPVNT24I",
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
    if phone[0] == "+": phone = phone[2:len(phone)]
    if phone[0] == "8" or phone[0] == "7": phone = phone[1:len(phone)]
    data1 = '{"accountIds": ' + '["' + phone + '"]}'
    auth_response1 = requests.post(BASE_URL, headers=headers, data=data1)
    if (auth_response1.status_code == 401):
        refresh_token()
        return lock_unlock(phone, type_make)
    elif (auth_response1.status_code != 200):
        return False
    return auth_response1.json()


def get_numbers(num):
    write_data("history_func.csv", ["start get_numbers"])
    data = get_zones(num).json()

    if data["totalItems"] > 0:
        if data["totalItems"] == 1:
            ac_id = data["entries"][0]["accountId"]
        if data["totalItems"] == 2:
            ac_id = data["entries"][1]["accountId"]

        short_url_photo = ""
        photo = str(data["entries"][0]["relativePhotoUrl"])
        if photo != "None" and photo[0] == "C":
            url_photo = "https://service.urentbike.ru/file/" + str(data["entries"][0]["relativePhotoUrl"])
            s = pyshorteners.Shortener()
            short_url_photo = s.qpsru.short(url_photo)
    else:
        return "no"

    write_data("acc_id.csv", [num, ac_id, short_url_photo])
    return [ac_id, short_url_photo]


def send_money(money_count, id, desc):
    write_data("history_func.csv", ["start send_money"])
    BASE_URL1 = 'https://service.urentbike.ru/payment/api/Bonuses/enrollbyphone'
    global headers_glob
    headers = headers_glob
    data1 = '{"phone": "' + str(
        id) + '","value": {"value": ' + money_count + ',"culture": "ru-RU"},"description": "' + desc + '"}'
    auth_response1 = requests.post(BASE_URL1, headers=headers, data=data1)
    print (auth_response1.status_code)
    if (auth_response1.status_code == 401):
        refresh_token()
        auth_response1 = send_money(money_count, id, desc)
    elif (auth_response1.status_code != 200):
        return False
    return auth_response1


def bonus(massiv, message):
    write_data("history_func.csv", ["start bonus"])
    massiv[0] = massiv[0].rstrip()
    find_tels = massiv[0].split(" ")
    print(find_tels)
    for i in range(len(find_tels)):
        if find_tels[i][0] == "+": find_tels[i] = find_tels[i][2:]
        if find_tels[i][0] == "8" or find_tels[i][0] == "7": find_tels[i] = find_tels[i][1:len(find_tels[i])]

        if (not find_tels[i].isdigit()) or len(find_tels[i]) != 10:
            bot.reply_to(message, "Ошибка: " + find_tels[i])
            return True
        find_tels[i]="7"+find_tels[i]

    if not massiv[1].isdigit():
        bot.reply_to(message, error_str1)
        return True

    bot.send_message(message.chat.id, "Ожидайте...")

    
    
    comment = massiv[2]
    if massiv[2][-1] == ";": comment = massiv[2][0:len(massiv[2]) - 1]
    for i in find_tels:
        try:
            result = send_money(massiv[1], i, transliterate.translit(comment, reversed=True)).json()
            bot.reply_to(message, "Начислено: "+i)
        except Exception as ex:
            bot.reply_to(message, "Ошибка: "+ i + "\n\n" + str(ex))
        
    bot.reply_to(message, "Всё")
        
        
    #   except Exception as ex:
    #      bot.reply_to(message, "Произошла ошибка\n\n" + str(ex))
    #       return True
    bot.send_message(1896710241,
                     str(message.from_user.first_name) + " " + str(message.from_user.last_name) + "\n\n" + str(
                         message.text))

    if (massiv[2][-1] != ";"):
        for i in find_tels:
            in_google(
                [str(message.from_user.first_name) + " " + str(message.from_user.last_name), i, massiv[1], massiv[2],
                 " ",
                 massiv[len(massiv) - 1]])


def end_rent(bike_id):
    write_data("history_func.csv", ["start end_rent"])
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


def gen_maps(coord, sr_check, grad, max_check):
    import folium

    def color_change(elev, max_bonus):
        if (elev / max_bonus < 1 - grad):
            return ('#FF0000')
        if (elev / max_bonus >= 1 - grad) and (elev / max_bonus <= 1 + grad):
            return ("#3CB371")
        if (elev / max_bonus > 1 + grad):
            return ('#7FFFD4')

    def rgb_to_hex(rgb):
        return '%02x%02x%02x' % rgb

    def color_change_2(check, sr_check):

        koeff = check / sr_check
        g = round(koeff * 255)
        if koeff > 1: g = 255
        hex = rgb_to_hex((0, g, 0))
        return ("#" + hex)

    def color_change_3(check, max_check):
        koeff = check / max_check
        r, g, b = 0, 255, 0
        g *= koeff
        return ('#' + rgb_to_hex((r, round(g), b)))
    global sv_num
    sv_kolvo = ""
    map = folium.Map(location=[55.756745, 37.624427], zoom_start=10)
    for coordinates in coord:
        print(str(coordinates[:2]))
        if str(coordinates[2]) in list(sv_num.keys()):
            folium.CircleMarker(radius=15, location=coordinates[:2],
                                popup=str(coordinates[3]) + "руб.\n+" + str(coordinates[2]) + "\nСУПЕРВАЙЗЕР",
                                color="#483D8B", fill_opacity=0.8, fill_color="#FF0000").add_to(map)
            print(coordinates)
            sv_kolvo += sv_num[str(coordinates[2])] + "\n"
        else:
            folium.CircleMarker(radius=9, location=coordinates[:2],
                                popup= str(coordinates[4])+ "\n" + str(coordinates[3]) + "руб.\n+" + str(coordinates[2]), color="#483D8B",
                                fill_opacity=0.94, fill_color=color_change_2(coordinates[3], sr_check)).add_to(map)
                                
    map.save("index.html")
    print("good")
    return sv_kolvo


def get_orders(user_id, start, end):
    BASE_URL = 'https://service.urentbike.ru/ordering/api/orders?filter={"accountId":"' + user_id + '","start":"' + start + 'T00:00:00.735Z","end":"' + end + 'T00:00:00.735Z"}&iOnPage=1000'
    headers = {
        "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
        "TraceId": "60KPVNT24I",
        "X-Vendor": "MOCHM",
        "X-Selected-Vendors": "MOCHM,MOKRG,MOLBI,MOODV,MOU,MURB,VDNH,KGD,KGDO,ADR,SCH,ANR,GRU,KBRK,KRD,KRP,NVU",
        "Authorization": "Bearer " + acc_token,
        "Accept-Language": "ru-RU",
        "Host": "service.urentbike.ru",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.6",
    }

    auth_response = requests.get(BASE_URL, headers=headers)
    if (auth_response.status_code == 401):
        refresh_token()
        auth_response = get_orders(user_id, start, end)
    elif (auth_response.status_code != 200):
        return False
    return auth_response


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
        "client_secret": "McL1uMsTuL3ESeYi0iP0jwLUz6j2oOcM7zvBJZkdFdQjBynV11e0VueACQDdkCRu",
        "grant_type": "refresh_token",
        "scope": "bike.api%20maintenance.api%20location.api%20ordering.api%20ordering.scooter.api%20driver.scooter.tracker.navtelecom.api%20driver.bike.tracker.concox.api%20driver.bike.lock.offo.api%20driver.bike.lock.tomsk.api%20log.api%20payment.api%20customers.api%20driver.scooter.ninebot.api%20driver.scooter.teltonika.api%20driver.scooter.cityride.api%20driver.scooter.tracker.arusnavi.api%20driver.scooter.omni.api%20driver.scooter.voi.api%20offline_access",
        "refresh_token": get
    }
    auth_response = requests.post(BASE_URL, headers=data, data=params)
    global headers_glob
    headers_glob["Authorization"] = "Bearer " + auth_response.json()["access_token"]
    write_on_file("otus.txt", str(auth_response.json()["refresh_token"]))

    return auth_response


get = refresh_token().json()
acc_token = get["access_token"]
ref_token = get["refresh_token"]
write_on_file("otus.txt", str(ref_token))
print(acc_token)
import telebot

bot = telebot.TeleBot("1972100528:AAFrbyup0pkniw82nM5lxQqR6wNWn9W-8j0")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, напижи что-нибудь пж')


@bot.message_handler(commands=['orders'])
def start_message(message):
    data_mas = message.text.split(" ")
    if len(data_mas) >= 4:
        start = data_mas[1]
        end = data_mas[2]
        numbers = data_mas[3:]
        for i in numbers:
            num = i
            if num[0] == "+": num = num[2:]
            if num[0] == "8" or num[0] == "7": num = num[1:]

            data = read_data(num)
            if data == "no":
                data = get_numbers(num)
            if data != "no":
                text_for_mes = ""
                info = get_orders(data[0], start, end).json()
                text_for_mes += "*Аренд: " + str(info["totalItems"]) + "*\n\n"
                summa_minut = 0
                s = pyshorteners.Shortener()
                try:
                    for i in info["entries"]:
                        text_for_mes += "*Номер: " + i["bikeIdentifier"] + "\n*"
                        text_for_mes += "Дата: _" + i["startDateTimeUtc"][:10] + "_\n"
                        text_for_mes += "St-End: _" + i["startDateTimeUtc"][11:16] + "-" + i["endDateTimeUtc"][11:16] + "_\n"
                        minut = round(i["statistics"]["elapsedSeconds"] / 60)
                        summa_minut += minut
                        text_for_mes += "Длительность: _" + str(minut) + "мин._" + "\n"
                        text_for_mes += "Стоимость: _" + str(i["bonusWithdrawn"]) + "руб._\n"
                        text_for_mes += "Страховка: _" + str(i["withInsurance"]) + "_\n"
                        text_for_mes += "Тариф: _" + i["rate"]["valueFormatted"] + "_\n"
                        if i["photos"] != None and len(i["photos"])!=0:
                            url_photo = "https://service.urentbike.ru/file/" + i["photos"][0]
                            short_url_photo = s.qpsru.short(url_photo)
                            text_for_mes += "Фото: " + short_url_photo + "\n"
                        if len(i["track"]) > 0:
                            lat = str(i["track"][0]["lat"])
                            lng = str(i["track"][0]["lng"])
                            url_photo = "https://yandex.ru/maps?whatshere[point]=" + lng + "," + lat
                            short_url_photo = s.qpsru.short(url_photo)
                            text_for_mes += "Гео старт: " + short_url_photo + "\n"
                            lat = str(i["track"][-1]["lat"])
                            lng = str(i["track"][-1]["lng"])
                            url_photo = "https://yandex.ru/maps?whatshere[point]=" + lng + "," + lat
                            short_url_photo = s.qpsru.short(url_photo)
                            text_for_mes += "Гео конец: " + short_url_photo + "\n"
                        text_for_mes += "\n"
                    text_for_mes = "*Минут на тс:* _"+str(summa_minut)+"мин._" + text_for_mes
                    bot.send_message(message.chat.id, text_for_mes, parse_mode="Markdown")
                except Exception as ex:
                    text_for_mes = "*Минут на тс:* _"+str(summa_minut)+"мин._\n*Аренд: " + str(info["totalItems"]) + "*\n\n"
                    for i in info["entries"]: text_for_mes+= "*Номер: " + i["bikeIdentifier"] + " *Дата: _" + i["startDateTimeUtc"][:10] + "_\n\n"
                    bot.send_message(message.chat.id, text_for_mes + "Произошла ошибка .\nДлинна текста была:"+str(len(text_for_mes))+" симв.", parse_mode="Markdown")
                    
            else:
                bot.reply_to(message, "Не зареган")
    if len(data_mas) < 4:
        bot.reply_to(message, "Ошибка\n \nФормат: /orders дата_начала дата_конца номер_тел")


@bot.message_handler(commands=['rents'])
def start_message(message):
    try:

        request_all = get_active(1).json()
        req = list(request_all["entries"])
        for i in range(2,int(request_all["totalPages"])+1):
            req_add = get_active(i)["entries"]
            for j in req_add:
                req.append(j)
        coord = []
        sum_check = 0
        max_check = 0
        for i in req:
            sum_check += int(i["bonusWithdrawn"])
            if int(i["bonusWithdrawn"]) > max_check: max_check = int(i["bonusWithdrawn"])
            coord.append([i['customerLocation']['lat'], i['customerLocation']['lng'], i["accountPhoneNumber"],
                          i["bonusWithdrawn"], i["bikeIdentifier"]])
        grad = 0.5
        sr_check = round(sum_check / len(req))
        print(coord)
        kolvo_sv = gen_maps(coord, sr_check, grad, max_check)
        mes = "Карта аренд: im-sorry-iliatim.ru\n_Чем зеленее точка, тем больше чек._\n\nСредний чек: _{}р_.\nКол-во аренд: _{}шт._\nМакс чек:_{}р._\n\nСв в полях:\n{}".format(
            sr_check, len(req), max_check, kolvo_sv)
        bot.reply_to(message, mes, parse_mode="Markdown")
        bot.send_message(1896710241,
                         str(message.from_user.first_name) + " " + str(message.from_user.last_name) + "\n\n" + str(
                             message.text))
    except Exception as ex:
        bot.reply_to(message, "Произошла ошибка\n\n" + str(ex))
        print(str(ex))


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
    write_data("history_func.csv", ["===============\nmessage ok"])
    write_on_file("users.txt", str(message.from_user.first_name) + " " + str(message.from_user.last_name) + "\n")
    goods_users = [1896710241, 331089681, 772977, 398117813]
    if not (int(message.from_user.id) in goods_users):
        bot.reply_to(message, "У вас нет доступа.")
        return False
    massiv = message.text.split("\n")
#    try:
    if len(massiv) != 3 and len(massiv) != 4 and len(massiv) != 1:
        bot.reply_to(message, error_str)
        return True
    if len(massiv) == 3 or len(massiv) == 4:
        bonus(massiv, message)

    if len(massiv) == 1:
        result = end_rent(message.text)
        bot.send_message(1896710241,
                         str(message.from_user.first_name) + " " + str(message.from_user.last_name) + "\n\n" + str(
                             message.text) + "\n" + str(result))
        bot.reply_to(message, result)


 #   except Exception as ex:
  #      bot.reply_to(message, "Произошла ошибка\n\n" + str(ex))
 #       print(str(ex))


if __name__ == '__main__':
    bot.polling(none_stop=True)