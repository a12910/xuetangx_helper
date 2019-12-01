import base64, json, pdb
import homeworks_head as head
import homeworks_db as db

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

def login():
    index, captcha_key= parse_index()

    url, header = head.get_header({
        'Referer': '?redirect=%2F%3Fredirect%3D%252F%253Fredirect%253D%25252F%252523%25252Fhome%2523%252Fhome%23%2Fhome',
        'x-referer': '?redirect=%2F%3Fredirect%3D%252F%253Fredirect%253D%25252F%252523%25252Fhome%2523%252Fhome%23%2Fhome#/home',
        'url': 'api/v1/oauth/number/login'
    }, {
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'If-Modified-Since': '0',
        'Origin':'https://nkdx.xuetangx.com'
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
    result_text = json.loads(result.text)
    if not result_text['return_code'] == 200:
        print('<登陆失败>')
        return False
    else:
        print('<登陆成功>')
    update_cookie(result)
    db.save_conf(False)

    return True

def update_cookie(result):
    result_head = result.headers
    # result_head = json.loads(result.headers)
    cookie0 = db.user_info['Cookie']
    cookie0 = cookie_parse(cookie0)
    # cookie0 = {}
    print('cookie0', db.user_info['Cookie'])
    for key in result_head.keys():
        # if not key.find('Set-Cookie')==-1:
        if key == 'Set-Cookie':
            cookie0.update(cookie_parse(result_head[key]))
    db.user_info['Cookie'] = cookie_parseout(cookie0)
    print('cookie1', db.user_info['Cookie'])
    # pdb.set_trace()

def cookie_parse(string):
    result = {}
    string = string.replace(' ', '')
    string = string.replace(' httponly, ', '')
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
        key2 = key.replace(' ', '')
        string += key + '=' + cookie_dict[key] + ';'

    string = string.replace('  ', '')[:-1]
    print('new cookie ', string)

    return string

if __name__ == '__main__':
    pass