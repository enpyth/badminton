import argparse
import configparser
import time
import requests
import json
import datetime
import threading


class Config:
    def __init__(self, path):
        self.path = path

    # 获取ini配置转为dict
    def get_config(self):
        config = configparser.RawConfigParser()
        # read ini config
        config.read(self.path)
        section = config.sections()

        # serialize config
        res = []
        for u in section:
            user = config[u]['user']
            login = config[u]['login']
            pwd = config[u]['pwd']
            cookie = config[u]['cookie']
            s1 = config[u]['schedule1']
            s2 = config[u]['schedule2']
            court = config[u]['court']
            delay = config[u]['delay']
            info = {
                'user': user,
                'login': login,
                'pwd': pwd,
                'cookie': cookie,
                'schedule1': s1,
                'schedule2': s2,
                'court': court,
                'delay': delay
            }
            res.append(info)
        return res

    # ini配置中更新cookie
    def update_config(self):
        config = configparser.RawConfigParser()
        config.read(self.path)
        section = config.sections()
        p = Property()
        # config user cookie
        for u in section:
            user = config[u]['user']
            login = config[u]['login']
            user_pwd = {"username": user, "password": login}
            cookie = p.get_lasted_cookie(user_pwd)
            print(f"{user} : {cookie}")
            config.set(user, 'cookie', cookie)

        with open(self.path, 'w') as file:
            config.write(file)


class Property:
    def __init__(self):
        self.schedules = {'7': '4c7006a8-64b4-4534-9200-b51c9161b63a',
                          '8': '04f3d042-1cf5-4a17-84cb-51f83e654ded',
                          '9': '78154bb0-53f6-47eb-a3a6-00a60779d2ae',
                          '10': '1f5b1523-bda3-4e3e-b8b6-88cea4f25cbe',
                          '11': '9394630a-62c6-4cb3-920c-ac21460635fd',
                          '12': 'c8a3009d-e01e-466a-be93-1ed2b93fa91f',
                          '13': '5a47103e-9810-40c4-a2c7-fa4d143638db',
                          '14': 'b1c73029-d196-4eff-849c-567b94ab7b4a',
                          '15': '90b95651-2587-4cc6-964b-b03417eaf992',
                          '16': '6e2fbb46-1e59-4ee9-82cb-5fcce59bc6c9',
                          '17': '58e1365a-5fda-4e4e-93c1-8f1714f7526e',
                          '18': 'c989302d-a79e-4510-8691-c2d76cdc5a1d',
                          '19': '25cc954e-35db-4d9a-8d5a-106e523ab092',
                          '20': '9f2f88fa-86cb-4311-a2ca-c08d99acf2a3',
                          '21': '7d6c5596-11bd-47a8-b306-1e799fcaf578',
                          '22': '2d05ec47-a357-44ec-94c4-9688159deb96',
                          }
        self.court = 'd0427041-e0bd-42ba-b58c-503cdb822379'
        self.url_login = "http://www.yanlordlife.cn/api/front/member/login"
        self.url_book = "http://www.yanlordlife.cn/api/front/member/booking"
        self.url_run = "http://www.yanlordlife.cn/api/front/club/venue/booking"

    # 通过时刻获取时刻序列
    def get_schedule(self, n):
        if str(n) not in self.schedules.keys():
            print(f"illegal schedule, check '{n}'.")
            exit(1)

        return self.schedules[str(n)]

    # 通过场号获取场地序列
    def get_court(self, n):
        court = self.court
        if str(n) == "2":
            court = 'f386ccf9-0a31-431d-9e94-e4d90d3f31ee'
        return court

    # 通过用户信息获取最新cookie
    def get_lasted_cookie(self, user_info):
        # url = "http://www.yanlordlife.cn/api/front/member/login"
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'www.yanlordlife.cn',
            'Origin': 'http://www.yanlordlife.cn',
        }
        r = requests.post(self.url_login, data=json.dumps(user_info), headers=header)

        if r.status_code == 200:
            return "connect.sid=" + r.cookies.get("connect.sid")
        return ""

    # 通过cookie查询用户的预订结果
    def property_select_booking(self, cookie):
        # url = 'http://www.yanlordlife.cn/api/front/member/booking'

        # payloadData数据
        # 羽毛球, 日期, 场地, 时间段, 密码

        pay_data = {"type": "1", }

        # 请求头设置
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': cookie,
            'Host': 'www.yanlordlife.cn',
            'Origin': 'http://www.yanlordlife.cn',
            'Referer': 'http://www.yanlordlife.cn/stadium/booking-list'
        }

        r = requests.post(self.url_book, data=json.dumps(pay_data), headers=header)
        if r.status_code == 200:
            return f"responseTime = {datetime.datetime.now()}, res text = {r.text}"
        else:
            return "查询失败"

    # 通过用户信息、预订信息发送预订请求
    def property_run_booking(self, date, cookie, pwd, schedule, court, delay):
        url = self.url_book
        print(datetime.datetime.now(), url)
        time.sleep(int(delay))
        print(f"function() {date} {cookie} {pwd} {schedule} {court}")

    def old_run_book(self, date, cookie, pwd, schedule, court, delay):
        url = self.url_run
        pay_data = {"venueId": "adabcf6a-280c-4098-97ef-5bb50c3c5184",
                    "bookingDate": date,
                    "courtId": court,
                    "schedules": [schedule],
                    "password": pwd}
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': cookie,
            'Host': 'www.yanlordlife.cn',
            'Origin': 'http://www.yanlordlife.cn',
            'Referer': 'http://www.yanlordlife.cn/stadium/booking/adabcf6a-280c-4098-97ef-5bb50c3c5184',
        }
        time.sleep(int(delay))
        r = requests.post(url, data=json.dumps(pay_data), headers=header)
        print(f"responseTime = {datetime.datetime.now()}, statusCode = {r.status_code}, res text = {r.text}, res:{r}")


class Subscribe:
    def __init__(self, path):
        self.path = path

    # 查询用户预订情况
    def select_status(self):
        config = Config(self.path).get_config()
        p = Property()
        for u in config:
            cookie = u['cookie']
            user = u['user']
            user_status = p.property_select_booking(cookie)
            print(f"{user} :\n{user_status}\n")

    # 通过配置获取序列化配置
    def trans_config(self):
        config = Config(self.path).get_config()
        p = Property()
        res = []
        for c in config:
            user = c['user']
            cookie = c['cookie']
            pwd = c['pwd']
            court = p.get_court(c['court'])
            s1 = c['schedule1']
            s2 = c['schedule2']
            delay = c['delay']
            if s1 == '0' and s2 == '0':
                continue
            if s1 != '0':
                info = {
                    'user': user,
                    'cookie': cookie,
                    'pwd': pwd,
                    'schedule': p.get_schedule(s1),
                    'court': court,
                    'delay': delay
                }
                res.append(info)
            if s2 != '0':
                info = {
                    'user': user,
                    'cookie': cookie,
                    'pwd': pwd,
                    'schedule': p.get_schedule(s2),
                    'court': court,
                    'delay': delay
                }
                res.append(info)
        return res

    # 并发预订
    def run_book(self, date):
        config = self.trans_config()
        p = Property()
        thread = []
        for c in config:
            cookie = c['cookie']
            pwd = c['pwd']
            schedule = c['schedule']
            court = c['court']
            delay = c['delay']
            thread.append(threading.Thread(target=p.old_run_book, args=(date, cookie, pwd, schedule, court, delay)))
        for t in thread:
            t.start()


def get_time():
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    _wait_date = (now + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    _book_date = (now + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    return _wait_date, _book_date


def get_rush_time():
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    _wait_date = (now + datetime.timedelta(days=0)).strftime('%Y-%m-%d')
    _book_date = (now + datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    return _wait_date, _book_date


if __name__ == '__main__':
    ini = "./config.ini"
    parser = argparse.ArgumentParser('zs')
    parser.add_argument('-m', default='help', help='login / status / test / rush')
    arg = parser.parse_args()
    # 模拟登陆，刷新cookie
    if arg.m == "login":
        ini_info = Config(ini)
        ini_info.update_config()
    # 查看用户预订信息
    elif arg.m == "status":
        sb = Subscribe(ini)
        sb.select_status()
    # test
    elif arg.m == "test":
        ini_info = Config(ini)
        sb = Subscribe(ini)

        wait_date, book_date = get_time()
        while 1:
            now = datetime.datetime.now()
            now_date = datetime.datetime.now().strftime('%Y-%m-%d')
            if now_date == wait_date:
                # RUN BOOK
                sb.run_book(book_date)
                break
            else:
                print(f'wait {wait_date}, now is {now}')
                time.sleep(1)

    elif arg.m == "rush":
        ini_info = Config(ini)
        sb = Subscribe(ini)

        wait_date, book_date = get_rush_time()
        while 1:
            now = datetime.datetime.now()
            now_date = datetime.datetime.now().strftime('%Y-%m-%d')
            if now_date == wait_date:
                # RUN BOOK
                sb.run_book(book_date)
                break
            else:
                print(f'wait {wait_date}, now is {now}')
                time.sleep(1)
    else:
        print("--help")

