import base64, json, pdb
import homeworks_head as head
import homeworks_db as db
from selenium import webdriver


def parse_index():
    '''验证码登陆'''
    url, header = head.get_header({
        'Referer': '?redirect=%2F%3Fredirect%3D%252F%253Fredirect%253D%25252F%252523%25252Fhome%2523%252Fhome%23%2Fhome',
        'x-referer': '?redirect=%2F%3Fredirect%3D%252F%2523%252Fhome%23%2Fhome#/home',
        'url': 'api/v1/code/captcha'
    }, {
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'If-Modified-Since': '0'
    })
    params = {
        'term_id': db.user_info['term_id'],
        'page_size': 10,
        'running_status': '',
        'search': '',
        'page': '1',
        'course_type': ''
    }
    result = head.send_data(url, params, header)
    result_text = json.loads(result.text)
    img = result_text['data']['img']
    with open('index.png', 'wb') as f:
        f.write(base64.b64decode(img))
    from PIL import Image
    im = Image.open('index.png')
    im.show()

    index = input('请输入验证码 ').replace('\n','')
    print('<正在登陆>')
    return index, result_text['data']['captcha_key']

def login(mode = ''):
    if mode == '' and login_test():
        return True

    db.user_info['temp_cookie'] = update_cookie2()
    index, captcha_key= parse_index()
    url, header = head.get_header({
        'Referer': '?redirect=%2F%3Fredirect%3D%252F%253Fredirect%253D%25252F%252523%25252Fhome%2523%252Fhome%23%2Fhome',
        'x-referer': '?redirect=%2F%3Fredirect%3D%252F%253Fredirect%253D%25252F%252523%25252Fhome%2523%252Fhome%23%2Fhome#/home',
        'url': 'api/v1/oauth/number/login'
    }, {
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'If-Modified-Since': '0',
        'Origin':'https://nkdx.xuetangx.com',
        'Cookie':db.user_info['Cookie']
    })
    params = {
        'captcha':index,
        'captcha_key':captcha_key,
        'is_alliance':'0',
        'login':db.user_info['user'],
        'password':db.user_info['passwd']
    }
    result = head.send_data_post(url, params, header)
    # pdb.set_trace()
    db.user_info['Cookie'] = update_cookie(result)
    result_text = json.loads(result.text)
    if not result_text['return_code'] == 200:
        print('<登陆失败>')
        return False
    else:
        return login_test()


def login_test():
    user_info = db.user_info
    url, header = head.get_header({
        'Referer': 'manager',
        'x-referer': 'manager#/teachercourselist',
        'url': 'course_manage_list'
    }, {
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'If-Modified-Since': '0'
    })
    params = {
        'term_id': user_info['term_id'],
        'page_size': 10,
        'running_status': '',
        'search': '',
        'page': '1',
        'course_type': ''

    }
    result = head.send_data(url, params, header)

    result_text = json.loads(result.text)
    # print(result_text)
    if not ('return_code' in result_text and result_text['return_code'] != 200) :
        print('<登陆成功>')
        db.save_conf(False)
        return True
    else:
        print('<登陆失败>')
        return False


def update_cookie2():
    print('<获取Cookie>')
    option = webdriver.FirefoxOptions()
    option.add_argument('--headless')
    driver = webdriver.Firefox(options=option)
    driver.get('http://nkdx.xuetangx.com')
    cookie = driver.get_cookies()
    result = {}
    for item in cookie:
        # result += str(item['name']) + '=' + str(item['value']) + ';'
        if item['name'].find('CNZZD') != -1:
            item['value'] = item['value'][:22] + 'https%253A%252F%252Fnkdx.xuetangx.com%252F' + item['value'][22:]
        result.update({
            item['name']:str(item['value'])
        })
    # print(result)
    return result


def update_cookie(result):
    result_head = result.headers
    # result_head = json.loads(result.headers)
    cookie0 = db.user_info['temp_cookie']
    # cookie0 = cookie_parse(cookie0)
    # cookie0 = {}
    # print(cookie0)
    for key in result_head.keys():
        # if not key.find('Set-Cookie')==-1:
        if key == 'Set-Cookie':
            cookie0.update(cookie_parse(result_head[key]))
    return cookie_parseout(cookie0)
    # pdb.set_trace()

def cookie_parse(string):
    result = {}
    # print(string)
    errs = ['', 'httponly,', 'path=/;']
    for item in errs:
        string = string.replace(item, '')

    while len(string)>0:
        equ = string.find('=')
        value0 = string.find(';')
        key = string[:equ]
        if equ == -1:
            # print(string)
            string = ''
            continue
        if value0 == -1:
            value = string[equ+1:]
            string = ''
        else:
            value = string[equ+1:value0]
            string = string[value0 + 1:]


        if not value == '':
            result.update({
                key:value
            })

    # print(result)
    return result


def cookie_parseout(cookie_dict):
    string = ''
    for key in cookie_dict.keys():
        # key2 = key.replace(' ', '')
        if key == 'expires':
            continue
        string += key + '=' + cookie_dict[key] + ';'

    string = string.replace('  ', '')[:-1]
    # print('new cookie ', string)

    return string

def test_cookie():
    option = webdriver.FirefoxOptions()
    option.add_argument('--headless')
    driver = webdriver.Firefox(options=option)
    driver.get('http://nkdx.xuetangx.com')
    cookie = driver.get_cookies()
    return cookie



if __name__ == '__main__':
    c1 = test_cookie()
    strr = "access_token=; path=/; expires=Mon, 13 Oct 1975 03:13:00 GMT; httponly, xt=; path=/; expires=Mon, 13 Oct 1975 03:13:00 GMT; httponly, xt_expires_in=; path=/; expires=Mon, 13 Oct 1975 03:13:00 GMT; httponly, identity=; path=/; expires=Mon, 13 Oct 1975 03:13:00 GMT; httponly, has_init_pwd=; path=/; expires=Mon, 13 Oct 1975 03:13:00 GMT; httponly, xt_auth=; path=/; expires=Mon, 13 Oct 1975 03:13:00 GMT; httponly, access_token=gAAAAABd42lcnzKejKGugLOyMP33RfDtCiCyHC8CsjXIazMnSppIfQbCR8n7TaOdYIb63Nv8Bi0Ua62qrkKsjhCAr6EljRid94pAPESXjWhhVbepuEEBSWY; path=/; expires=Sun, 01 Dec 2019 09:19:42 GMT; domain=xuetangx.com; httponly, xt=gAAAAABd42lccDPTTD07yODSNG1HnQWbNMOXdBgDsWB3K8PNUrd0GP3iJTRuqjUlY54AzaH9JQgFmDWEFnBAfVOMqS8TReXG86raoNVGAmHQ0HBytUli6ns; path=/; expires=Sun, 08 Dec 2019 07:19:42 GMT; domain=xuetangx.com; httponly, xt_expires_in=604800; path=/; expires=Sun, 08 Dec 2019 07:19:42 GMT; domain=xuetangx.com; httponly, identity=3; path=/; expires=Sun, 08 Dec 2019 07:19:42 GMT; domain=xuetangx.com, has_init_pwd=; path=/; expires=Mon, 13 Oct 1975 03:13:00 GMT; domain=xuetangx.com; httponly', 'Cache-Control': 'no-cache,max-age=0', 'Content-Encoding': 'gzip'"
    c2 = cookie_parse(strr)
    c1.update(c2)
    # print(c1)
    pass