import requests
import hashlib
import time
import random
from datetime import datetime
from lequangminh import *

def register_facebook_account():
    app = {
        'api_key': '882a8490361da98702bf97a021ddc14d',
        'secret': '62f8ce9f74b12f84c123cc23437a4a32'
    }
    email_prefix = [
        'gmail.com',
        'hotmail.com',
        'yahoo.com',
        'outlook.com',
    ]
    names = {
        'first': [
            'JAMES', 'JOHN', 'ROBERT', 'MICHAEL', 'WILLIAM', 'DAVID',
        ],
        'last': [
            'SMITH', 'JOHNSON', 'WILLIAMS', 'BROWN', 'JONES', 'MILLER'
        ],
        'mid': [
            'Alexander', 'Anthony', 'Charles', 'Dash', 'David', 'Edward'
        ]
    }
    password = 'lequangminh@'
    random_birth_day = datetime.fromtimestamp(random.randint(time.mktime(datetime(1990, 1, 1).timetuple()), time.mktime(datetime(2005, 12, 30).timetuple()))).strftime('%d-%m-%Y')
    random_first_name = random.choice(names['first'])
    random_name = random.choice(names['mid']) + ' ' + random.choice(names['last'])
    full_name = random_first_name + ' ' + random_name
    md5_time = hashlib.md5(str(time.time()).encode()).hexdigest()
    hash_val = '-'.join([md5_time[:8], md5_time[8:12], md5_time[12:16], md5_time[16:20], md5_time[20:]])
    email_rand = ''.join(full_name.split()).lower() + hashlib.md5((str(time.time()) + datetime.now().strftime('%Y%m%d') + str(random.randint(0, 9999))).encode()).hexdigest()[:6] + '@' + random.choice(email_prefix)
    gender = 'M' if random.randint(0, 10) > 5 else 'F'
    
    req = {
        'api_key': app['api_key'],
        'attempt_login': True,
        'birthday': random_birth_day,
        'client_country_code': 'VN',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': random_first_name,
        'format': 'json',
        'gender': gender,
        'lastname': random_name,
        'email': email_rand,
        'locale': 'vi_VN',
        'method': 'user.register',
        'password': password,
        'reg_instance': hash_val,
        'return_multiple_errors': True
    }
    
    sorted_req = dict(sorted(req.items()))
    sig = ''.join([f"{k}={v}" for k, v in sorted_req.items()])
    ensig = hashlib.md5((sig + app['secret']).encode()).hexdigest()
    req['sig'] = ensig
    
    api = 'https://b-api.facebook.com/method/user.register'
    reg = _call(api, req)
    return reg

def _call(url, params, post=1):
    headers = {
        'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/vi_VN;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]',
    }
    if post:
        response = requests.post(url, data=params, headers=headers)
    else:
        response = requests.get(url, params=params, headers=headers)
    response_data = response.json()
    normalized_cp = response_data.get('normalized_cp')
    new_user_id = response_data.get('new_user_id')
    password = response_data.get('password', 'lequangminh@')
    birthday = params['birthday']
    result = {
        'Mail': normalized_cp,
        'UID': new_user_id,
        'Password': password,
        'Birthday': birthday,
        'Full Name': params['firstname'] + ' ' + params['lastname'],
        'Gender': params['gender']
    }
    return result

def save_accounts_to_file(accounts, filename):
    with open(filename, 'a') as file:
        for account in accounts:
            file.write(f"Mail: {account['Mail']} - UID: {account['UID']} - Password: {account['Password']} - Birthday: {account['Birthday']} - Full Name: {account['Full Name']} - Gender: {account['Gender']}\n")

if __name__ == "__main__":
    num_accounts = int(input(Colorate.Horizontal(Colors.red_to_white, f'NHẬP SỐ LƯỢNG TÀI KHOẢN CẦN TẠO: ')))
    accounts = []
    for _ in range(num_accounts):
        registration_info = register_facebook_account()
        accounts.append(registration_info)
        print(registration_info)
        # Chờ một khoảng thời gian ngẫu nhiên giữa mỗi lần đăng ký
        delay_seconds = random.randint(5, 15)  # Chờ từ 5 đến 15 giây
        print(Colorate.Horizontal(Colors.red_to_white,f"Chờ {delay_seconds} giây trước khi đăng ký tài khoản tiếp theo..."))
        time.sleep(delay_seconds)
    
    save_accounts_to_file(accounts, "acc.txt")
    print(Colorate.Horizontal(Colors.red_to_white,f"Thông tin tài khoản đã được lưu vào file 'acc.txt'"))
