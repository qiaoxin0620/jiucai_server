import datetime
import json
import time
from util.mysql_client import mc
import requests

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'PHPSESSID=kj3i6k8heitbtaotk0tr5pci51; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

# proxies = {
#     "http": "http://127.0.0.1:7890",
#     "https": "http://127.0.0.1:7890",
# }
proxies = None

def get_enc_timestamp():
    timestamp = int(time.time())
    url = f"http://127.0.0.1:3000/get_header_param?t={timestamp}"
    resp = requests.get(url)
    jd = json.loads(resp.text)
    if jd.get("code") == 200 and resp.status_code == 200:
        return timestamp,jd.get("headerTime")


def crawl_index(cid = "3"):
    for i in range(1,100):
        while True:
            try:
                t,ht = get_enc_timestamp()
                data = {
                    "cid":cid,
                    "page":i,
                    "kw":""
                }
                print(data)
                headers.update({"timestamp": ht})
                response = requests.post('https://jiucai.trwwhii.top/baseurl/api/public/?s=App.Tools.Index', headers=headers, data=data,proxies=proxies)
                has_more = parse_index(response.text,t)
                break
            except Exception as e:
                print(e)
        if not has_more:
            break

def crawl_detail(tid):
    while True:
        try:
            data = {
                'tid': str(tid)
            }
            t,ht = get_enc_timestamp()
            headers.update({"timestamp": ht})
            response = requests.post('https://jiucai.trwwhii.top/baseurl/api/public/?s=App.Tools.Info', headers=headers, data=data,timeout=10)
            data = parse_detail(response.text,t)
            jd = json.loads(data)
            title = jd.get("name")
            sales = jd.get("sales")
            desc = jd.get("desc")
            detail_items = {
                "tid":tid,
                "title":title,
                "sales":sales,
                "desc":desc,
            }
            if len(title) > 0 and len(desc) > 0:
                save_detail(detail_items)
                return
        except Exception as e:
            print(e)


def parse_detail(body,timestamp):
    try:
        headers = {'Content-Type': 'application/json'}
        body = json.loads(body).get("data")
        data = {"data":body,"timestamp":timestamp}
        url = "http://127.0.0.1:3000/data"
        response = requests.request("POST", url, headers=headers, data=json.dumps(data))
        jd = json.loads(response.text)

        if jd.get("code") == 200:
            data = jd.get("data")
            return data

    except Exception as e:
        print("解析列表页出错")

def save_index(items):
    conn,cursor = mc.getConn()
    for item in items:
        try:
            tid = item.get("tid")
            cid = item.get("cid")
            sort = item.get("sort")
            name = item.get("name")
            shop_img = item.get("shopimg")
            price = item.get("price")
            addtime = item.get("addtime")
            sql = f"insert ignore into items(tid,cid,sort,name,shop_img,price,add_time) values ({tid},{cid},{sort},'{name}','{shop_img}',{float(price)},'{addtime}')"
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)
    mc.dispose(conn,cursor)

def save_detail(item):
    conn,cursor = mc.getConn()
    try:
        tid = item.get("tid")
        title = item.get("title")
        desc = item.get("desc")
        sales = item.get("sales")
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = f"insert ignore into detail(tid,title,`desc`,sales,create_time) values ({tid},'{title}','{desc}',{sales},'{create_time}')"
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    mc.dispose(conn,cursor)

def parse_index(body,timestamp):
    try:
        headers = {'Content-Type': 'application/json'}
        body = json.loads(body).get("data")
        data = {"data":body,"timestamp":timestamp}
        url = "http://127.0.0.1:3000/data"
        response = requests.request("POST", url, headers=headers, data=json.dumps(data))
        jd = json.loads(response.text)
        if jd.get("code") == 200:
            itemsStr = jd.get("data")
            if len(itemsStr) > 0:
                items = json.loads(itemsStr)
                datas = items.get("data")
                save_index(datas)
                if len(datas) == 10:
                    return True
                # crawl_detail()
                # print(items)
    except Exception as e:
        print("解析列表页出错")


def select_tids():
    conn,cursor = mc.getConn()
    try:
        sql = f"select tid from items where crawled is null"
        print(sql)
        cursor.execute(sql)
        tids = cursor.fetchall()
        return tids
    except Exception as e:
        print(e)
    finally:
        mc.dispose(conn,cursor)


if __name__ == '__main__':
    tids = select_tids()
    for i in tids:
        crawl_detail(i.get("tid"))
    # crawl_index()