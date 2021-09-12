import datetime


def get_schedule(n):
    schedules = {'7': '4c7006a8-64b4-4534-9200-b51c9161b63a',
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
    return schedules[str(n)]


def run_book(date, cookie, pwd, schedule):
    url = 'http://www.yanlordlife.cn/api/front/club/venue/booking'

    # payloadData数据
    # 羽毛球, 日期, 场地, 时间段, 密码

    pay_data = {"venueId": "adabcf6a-280c-4098-97ef-5bb50c3c5184",
                "bookingDate": date,
                "courtId": "d0427041-e0bd-42ba-b58c-503cdb822379",
                "schedules": [get_schedule(schedule)],
                "password": pwd}

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
        'Referer': 'http://www.yanlordlife.cn/stadium/booking/adabcf6a-280c-4098-97ef-5bb50c3c5184',
    }

    print(pay_data)

def run_book_new(date, cookie, pwd, *schedules):
    url = 'http://www.yanlordlife.cn/api/front/club/venue/booking'

    # payloadData数据
    # 羽毛球, 日期, 场地, 时间段, 密码
    tmp = [get_schedule(item) for item in schedules]
    pay_data = {"venueId": "adabcf6a-280c-4098-97ef-5bb50c3c5184",
                "bookingDate": date,
                "courtId": "d0427041-e0bd-42ba-b58c-503cdb822379",
                "schedules": tmp,
                "password": pwd}

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
        'Referer': 'http://www.yanlordlife.cn/stadium/booking/adabcf6a-280c-4098-97ef-5bb50c3c5184',
    }

    print(pay_data)



def run():
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    wait_date = (now + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    book_date = (now + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    print(f'now_date:  {now_date}')
    print(f'wait_date: {wait_date}')
    print(f'book_date: {book_date}')

    # tiss1 / jspark79
    book_cookie = 'connect.sid=s%3A2BrAR8JyXEiqVXSxcFrHVrVnKqoWMrZ4.tOt56tarwOnYJdTeqBHUGbAtAIr%2FFyG%2FhHIc8PtNTa8'
    book_schedule = '18'
    book_schedule2 = '19'

    run_book(book_date, book_cookie, 'pwd', book_schedule)
    run_book(book_date, book_cookie, 'pwd', book_schedule2)
    run_book_new(book_date, book_cookie, 'pwd', book_schedule)
    run_book_new(book_date, book_cookie, 'pwd', book_schedule2)
    run_book_new(book_date, book_cookie, 'pwd', book_schedule, book_schedule2)


if __name__ == '__main__':
    run()
