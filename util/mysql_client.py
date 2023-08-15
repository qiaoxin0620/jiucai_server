# coding=utf-8
import datetime
import hashlib
import json
import re
from dbutils.pooled_db import PooledDB
from config import host, user, password, database, port
import time
import pymysql
from util.logger import log
from util.tools import get_current_time

"""
    mysql连接池 requests爬虫下使用
"""


class MysqlHelper(object):
    def __init__(self):
        self.__pool = PooledDB(creator=pymysql,
                               mincached=10,
                               maxcached=10,
                               maxshared=10,
                               maxconnections=10,
                               maxusage=100,
                               blocking=True,
                               user=user,
                               passwd=password,
                               db=database,
                               host=host,
                               port=port,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor
                               )

    def getConn(self):
        conn = self.__pool.connection()  # 从连接池获取一个链接
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def dispose(cursor, conn):
        cursor.close()
        conn.close()

    def get_job_item(self, data_source):
        """加载再点对应的所有招聘信息，做去重处理"""
        conn, cursor = self.getConn()
        cursor.execute(f"SELECT data_source,json_md5,job_id from zhaopin where data_source='{data_source}'")
        result_dict = cursor.fetchall()
        self.dispose(cursor, conn)
        return result_dict


    def save_zhaopin(self, data):
        jd = json.dumps(data)
        jd_md5 = hashlib.md5(jd.encode(encoding='UTF-8')).hexdigest()
        try:
            data_source = data.get("data_source","")
            job_id = data.get("job_id","")
            if not job_id:
                reg = re.search("job_detail/(.*?).htm",data.get("position_link","")).groups()
                if reg:
                    job_id = reg[0]
            conn, cursor = self.getConn()
            sql = "insert ignore into zhaopin(data_source,json_text,json_md5,job_id) values(%s, %s,%s,%s)"
            cursor.execute(sql, (data_source, jd, jd_md5,job_id))
            conn.commit()
        except Exception as e:
            log.error("save_zhaopin:{}".format(e))
        finally:
            self.dispose(cursor, conn)

    def get_city_codo_by_city_name(self,city_name):
        conn, cursor = self.getConn()
        try:
            sql = f"select city,area,city_code,area_code from zhaopin.city_code where city='{city_name}' and source_type='boss'"
            cursor.execute(sql)
            result_dict = cursor.fetchall()
            return result_dict
        except Exception as e:
            log.error("save_zhaopin:{}".format(e))
        finally:
            self.dispose(cursor, conn)

    def save_boss_data(self,items,table_name='boss'):
        conn, cursor = self.getConn()
        try:
            for item in items:
                url,query,city_code,area,job_id,site,page = item[0],item[1],item[2],item[3],item[4],item[5],item[6]
                sql = f"insert ignore into zhaopin.{table_name}(url,query,city_code,area_code,page,job_id,site,create_time) values ('{url}','{query}','{city_code}','{area}',{page},'{job_id}','{site}','{get_current_time()}')"
                cursor.execute(sql)
            conn.commit()
        except Exception as e:
            log.error("save_boss:{}".format(e))
        finally:
            self.dispose(cursor,conn)

    def update_boss_data(self,item,table_name='boss_task'):
        conn, cursor = self.getConn()
        try:
            res_count = item.get('res_count',0)
            site = item.get('site','')
            query = item.get('query','')
            area_code = item.get('area_code','')
            city_code = item.get('city_code','')
            task_time = item.get('task_time','')
            sql = f"update zhaopin.{table_name} set res_count={res_count},crawled=1 where site='{site}' and query='{query}' and area_code='{area_code}' and city_code='{city_code}' and task_time='{task_time}'"
            print(sql)
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            log.error("update_boss:{}".format(e))
        finally:
            self.dispose(cursor,conn)

    def update_boss_account(self,phone,step='start'):
        conn, cursor = self.getConn()
        try:
            end_time = datetime.datetime.now().strftime("%Y-%m-%d")
            sql = f"update zhaopin.boss_account set end_time='{end_time}' where phone='{phone}'"
            print(sql)
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            log.error("update_boss:{}".format(e))
        finally:
            self.dispose(cursor,conn)

    def select_boss_account(self):
        conn, cursor = self.getConn()
        try:
            sql = f"select phone,end_time from zhaopin.boss_account"
            cursor.execute(sql)
            result_dict = cursor.fetchall()
            return result_dict
        except Exception as e:
            log.error("update_boss:{}".format(e))
        finally:
            self.dispose(cursor,conn)


    def select_boss_task(self,site,query,table_name="boss_task"):
        conn, cursor = self.getConn()
        try:
            task_time = datetime.datetime.now().strftime("%Y-%m-%d")
            if query:
                sql = f"select site,query,city_code,area_code,city_name,area_name,task_time from zhaopin.{table_name} where task_time<='{task_time}' and crawled=0 and site='{site}' and query='{query}' ORDER BY task_time asc,res_count desc,city_level asc limit 100"
            else:
                sql = f"select site,query,city_code,area_code,city_name,area_name,task_time from zhaopin.{table_name} where task_time<='{task_time}' and crawled=0 and site='{site}' ORDER BY task_time asc,res_count desc,city_level asc limit 100"
            cursor.execute(sql)
            result_dict = cursor.fetchall()
            return result_dict
        except Exception as e:
            log.error("update_boss:{}".format(e))
        finally:
            self.dispose(cursor,conn)

    def update_boss_crawled_status(self,job_id,table_name="boss"):
        conn, cursor = self.getConn()
        try:
            update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_sql = f"update zhaopin.{table_name} set crawled=1,update_time='{update_time}' where job_id='{job_id}'"
            cursor.execute(update_sql)
            conn.commit()
        except Exception as e:
            log.error("update_boss crawled and update_time:{}".format(e))
        finally:
            self.dispose(cursor,conn)


mc = MysqlHelper()


if __name__ == "__main__":
    pass
    # mc.save_error_log({'sku': 'LA02-PC-C01-P243H(A)', 'asin': 'B07ZPKN6YR', 'marketCountry': 'US', 'shopName': 'LA02'}, '404')
    # print(mc.clear_cookie())
    # print(mc.select_today_error_asin())
    # from concurrent.futures import ThreadPoolExecutor
    #
    # thread_pool = ThreadPoolExecutor(11)
    #
    # for i in range(1):
    #     thread_pool.submit(mc.save_error_asin, {'sku': 'LA02-PC-C01-P243H(A)', 'asin': 'B07ZPKN6YR', 'marketCountry': 'US', 'shopName': 'LA02'}, '404')
    #
    # time.sleep(10)
