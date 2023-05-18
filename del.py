from work_token import requests_work
import pyshorteners,json


def go(num, start, end):
    print("start go")
    work = requests_work()
    print("gen token")
    data_id = work.find_customers(num).json()["entries"]
    print(len(data_id))
#    data_id = [{"accountId":"61841f12726b2dc225df80a9"}]
    print(data_id)
    if len(data_id) != 1:
        print("Что-то не так ", data_id)
        return True

    info = work.get_orders(data_id[0]["accountId"], start, end).json()
    print(json.dumps(info,indent=2))

    text_for_mes = "*Аренд: " + str(info["totalItems"]) + "*\n\n"
    summa_minut = 0
    s = pyshorteners.Shortener()
    for i in info["entries"]:
        text_for_mes += "Номер: " + i["bikeIdentifier"] + "\n*"
        text_for_mes += "Дата:" + i["startDateTimeUtc"][:10] + "\n"
        text_for_mes += "St-End:" + i["startDateTimeUtc"][11:16] + "-" + i["endDateTimeUtc"][11:16] + "_\n"
        minut = round(i["statistics"]["elapsedSeconds"] / 60)
        summa_minut += minut
        text_for_mes += "Длительность: _" + str(minut) + "мин._" + "\n"
        text_for_mes += "Стоимость: _" + str(i["bonusWithdrawn"]) + "руб._\n"
        text_for_mes += "Страховка: _" + str(i["withInsurance"]) + "_\n"
        text_for_mes += "Тариф:" + i["rate"]["valueFormatted"] + "_\n"
        if i["photos"] != None and len(i["photos"]) != 0:
            url_photo = "https://service.urentbike.ru/file/" + i["photos"][0]
            short_url_photo = url_photo
            text_for_mes += "Фото: " + short_url_photo + "\n"
        if len(i["track"]) > 0:
            lat = str(i["track"][0]["lat"])
            lng = str(i["track"][0]["lng"])
            url_photo = "https://yandex.ru/maps?whatshere[point]=" + lng + "," + lat
            short_url_photo = url_photo
            text_for_mes += "Гео старт: " + short_url_photo + "\n"
            lat = str(i["track"][-1]["lat"])
            lng = str(i["track"][-1]["lng"])
            url_photo = "https://yandex.ru/maps?whatshere[point]=" + lng + "," + lat
            short_url_photo = url_photo
            text_for_mes += "Гео конец: " + short_url_photo + "\n"
        text_for_mes += "\n"
    text_for_mes = "Минут на тс:" + str(summa_minut) + "мин." + text_for_mes
    return text_for_mes

print(go("79636247169", "2022-09-24", "2022-09-25"))

