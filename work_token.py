class requests_work:
    config = __import__("config")
    requests = __import__("requests")
    def __init__(self):
        self.acc_token = "Bearer " + self.refresh_token().json()["access_token"]
        print(self.acc_token)

    def write_on_file(self, name_file, ref):
        o_mode = "w"
        file = open(name_file, o_mode, encoding="utf-8")
        file.write(ref)
        file.close()
        return True

    def read_on_file(self):
        f = open(self.config.file_otus, encoding="utf-8")
        ref = f.readline()
        f.close()
        return ref

    def refresh_token(self):
        get = self.read_on_file()
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
        auth_response = self.requests.post(BASE_URL, headers=data, data=params)
        self.write_on_file(self.config.file_otus, str(auth_response.json()["refresh_token"]))
        return auth_response

    def get_active(self, cpage):
        BASE_URL = 'https://service.urentbike.ru/ordering/api/activity/all?cPage=' + str(cpage) + '&iOnPage=1000'
        headers = {
            "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
            "TraceId": "60KPVNT24I",
            "X-Vendor": "MOCHM",
            "X-Selected-Vendors": self.config.vendors,
            "Authorization": self.acc_token,
            "Accept-Language": "ru-RU",
            "Host": "service.urentbike.ru",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.6",
        }

        auth_response = self.requests.get(BASE_URL, headers=headers)
        if (auth_response.status_code == 401):
            get = self.refresh_token().json()
            self.acc_token = "Bearer " + get["access_token"]
            auth_response = self.get_active(cpage)
        elif (auth_response.status_code != 200):
            return False
        return auth_response

    def get_prostoi(self, mins):

        BASE_URL = 'https://service.urentbike.ru/bikes/api/bikes/list'

        ghost = "UseZoneIds=5f1ec73fb368150001243a48&UseZoneIds=60b626e75b4c4dd13840f5e5&UseZoneIds=5f1ec810b368150001344fa3&UseZoneIds=617938b1292e8f61c7ec051c&UseZoneIds=605f2284fe455fb5d786aee9&UseZoneIds=6278c9b3960cf0da5373ea8d&UseZoneIds=6234438db93d1de164044483&UseZoneIds=60d561aee616718b1261e76e&UseZoneIds=607c1b1beb18f95863765f3b&UseZoneIds=6257e88ee4329e0c139e037f&UseZoneIds=6278bca3567c3096760bb205&UseZoneIds=6278bf1a6876cfb99c6812a8&UseZoneIds=6278c91b9443b07c0aa32e50&UseZoneIds=626917de840b7d7541c56461&UseZoneIds=6278c7969a5b6ad8a73fae1a&UseZoneIds=623590272a517c64d8fdda3d&UseZoneIds=6278c6456876cfb99c6dca94&UseZoneIds=6278c84cd74d5cfda0daa59d&UseZoneIds=6239a2dedf794a3f2e113a6a&UseZoneIds=621f3d5a1364b49accb2e2f1&UseZoneIds=60e5c3a65c7e53537d5de0c0"
        BASE_URL += "?"+ghost+"ModelIds=603e6968f36b5b1d417d09b0&ModelIds=5cacf4da6b4e4400011c4216&ModelIds=603e6a17f36b5b1d417d7305&ModelIds=5cf22bb92f57960001d2c534&ModelIds=628632dac70ee8d786417ccc&ModelIds=624ed53c0f6f5ccfc0fe7779&ModelIds=605efed2d2239e65f021e39f&ModelIds=605f0280d2239e65f028ce5e&ModelIds=625ee5a9313aec3a7fc26678&ModelIds=617173dfc746de28dc4df233&ModelIds=5bf46bb4b852e60001681981&ModelIds=60bdccaf887c7f2d43a8c6b5&ModelIds=617816ccaf1cc840beb1e12a&ModelIds=5db92abb422036000178621a&ModelIds=60d5895f85266c18527ad05f&ModelIds=62725b3431023720c22f5403&ModelIds=60617c27ed77557dfbf8f6a9&ModelIds=60881599e33929fe8140403d&ModelIds=5f5b538d1af7340001dcaa9f&ModelIds=5f7b30a67522920001108ee6&ModelIds=606f22f42955f9ad88431409&ModelIds=60b0b4149e6b08ce05eaed7f&ModelIds=60b0b4799e6b08ce05eba870&ModelIds=5c28a721cb194a0001ca7d72&ModelIds=6245660a051894431a6dea09&IdleMins=" + str(mins)

        headers = {
            "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
            "TraceId": "60KPVNT24I",
            "X-Vendor": "MOCHM",
            "X-Selected-Vendors": self.config.vendors,
            "Authorization": self.acc_token,
            "Accept-Language": "ru-RU",
            "Host": "service.urentbike.ru",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.6",
        }
        auth_response = self.requests.get(BASE_URL, headers=headers)
        if (auth_response.status_code == 401):
            get = self.refresh_token().json()
            self.acc_token = "Bearer " + get["access_token"]
            auth_response = self.get_prostoi(mins)
        elif (auth_response.status_code != 200):
            return False
        return auth_response

    def get_orders(self, user_id, start, end):
        BASE_URL = 'https://service.urentbike.ru/ordering/api/orders?filter={"accountId":"' + user_id + '","start":"' + start + 'T00:00:00.735Z","end":"' + end + 'T00:00:00.735Z"}&iOnPage=1000'
        headers = {
            "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
            "TraceId": "60KPVNT24I",
            "X-Vendor": "MOCHM",
            "X-Selected-Vendors": "MOCHM,MOKRG,MOLBI,MOODV,MOU,MURB,VDNH,KGD,KGDO,ADR,SCH,ANR,GRU,KBRK,KRD,KRP,NVU,KGD,KGDO,SPP,SPPO",
            "Authorization": self.acc_token,
            "Accept-Language": "ru-RU",
            "Host": "service.urentbike.ru",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.6",
        }

        auth_response = self.requests.get(BASE_URL, headers=headers)
        if (auth_response.status_code == 401):
            get = self.refresh_token().json()
            self.acc_token = "Bearer " + get["access_token"]
            auth_response = self.get_orders(user_id,start,end)
        elif (auth_response.status_code != 200):
            print(auth_response.json())
            return False
        return auth_response

    def find_customers(self, num):
        BASE_URL = 'https://service.urentbike.ru/customers/api/customers?filter={"text":"' + num + '"}&cPage=1&iOnPage=10'

        headers = {
            "Environment-Info": "platform: TechAndroid, osVersion: 22, appVersion: 61.2 (16), device: Asus ASUS_Z01QD, phone: 79999696689",
            "TraceId": "BTOGUB8UZZ",
            "X-Vendor": "ADR",
            "X-Selected-Vendors": "ADR",
            "Authorization": self.acc_token,
            "Accept-Language": "ru-RU",
            "Host": "service.urentbike.ru",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.6",
            "Content-Type": "application/json"
        }


        auth_response = self.requests.get(BASE_URL, headers=headers)
        if (auth_response.status_code == 401):
            get = self.refresh_token().json()
            self.acc_token = "Bearer " + get["access_token"]
            auth_response = self.find_customers(num)
        elif (auth_response.status_code != 200):
            return False
        return auth_response