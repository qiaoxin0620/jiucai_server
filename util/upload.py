from util.logger import log
import requests
import json
from config import DOMAIN_ZHAOPIN,DOMAIN_GEEK,DOMAIN_QG
import re

from util.mysql_client import mc

'''
    加载job_item 到内存，用来去重岗位信息
'''
'''
    上传简历信息
'''
def upload_geek(job_item, data_source, source_site, source_type, company_name_reliable=0):
    url = DOMAIN_GEEK + '/home/public/addResumeInfo'
    data = {
        'company_name': job_item['company'],
        'position': job_item['position'],
        'company_description': job_item['info'],
        'data_source': data_source,
        'source_site': source_site,
        'source_type': source_type,
        'company_name_reliable': company_name_reliable
    }

    for i in range(3):
        try:
            response = requests.post(url, data=data, timeout=10)
            log.info("标题：{} 上传结果：{} {}".format(job_item['position'], response.status_code, response.text))
            return True
        except Exception as e:
            pass
    return False


'''
    上传招聘信息
'''


def upload(job_item, filter, data_source, source_site, source_type, company_name_reliable=0,site = "feikua"):
    if job_item is None:
        return

    if filter:
        for f in filter:
            if f in job_item.get("job_name", '').lower() or f in job_item.get("job_text", '').lower():
                break
        else:
            log.info('{}未包含关键词：{}'.format(job_item["job_name"], filter))
            return
    if site == "qg":
        url = DOMAIN_QG + '/home/public/addRecruitmentInfo'
    else:
        url = DOMAIN_ZHAOPIN + '/home/public/addRecruitmentInfo'
    data = {
        'company_name': job_item.get("company_name", ""),
        'industry': job_item.get("industry", ""),
        'city': job_item.get("city", ""),
        'scale': job_item.get("pnum", ""),
        'project': job_item.get("project_name", ""),
        'position': job_item["job_name"],
        'position_text': re.sub(u'['u'\U0001F300-\U0001F64F'u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55\U00010000-\U0010ffff]+', '', job_item.get("job_text", '')),
        'data_source': data_source,
        'position_link': job_item.get("job_href", ""),
        'company_link':  job_item.get("company_href", ""),
        'source_site': source_site,
        'source_type': source_type,
        'company_name_reliable': company_name_reliable,
        'job_id': job_item.get("job_id", ""),
    }
    mc.save_zhaopin(data)
    for i in range(3):
        try:
            response = requests.post(url, data=data, timeout=10)
            log.info("{}-{}-{}-{}-{}上传结果：{} {}".format(url,company_name_reliable, job_item.get("city", ""),
                                                    job_item["company_name"], job_item["job_name"],
                                                    response.status_code, response.text))
            return True
        except Exception as e:
            log.error("上传失败：{}".format(e))
            pass
    return False


'''
    更新状态
'''


def update_status(task_id, status,site="feikua"):
    if not task_id:
        return
    if site == "qg":
        url = DOMAIN_QG + '/home/public/UpdateSpiderTaskStatus'
    else:
        url = DOMAIN_ZHAOPIN + '/home/public/UpdateSpiderTaskStatus'

    data = {
        'id': task_id,
        'status': status
    }
    for i in range(3):
        try:
            resp = requests.post(url, data=data, timeout=10)
            if json.loads(resp.text)['result']:
                return True
            else:
                return False
        except Exception as e:
            pass
    return False


'''
    获取所有任务
'''


def get_task(site="feikua"):
    if site == "qg":
        url = DOMAIN_QG + "/home/public/ReadSpiderTask"
    else:
        url = DOMAIN_ZHAOPIN + "/home/public/ReadSpiderTask"
    for i in range(3):
        try:
            resp = requests.get(url, timeout=10)
            result = json.loads(resp.text)
            if result.get('result'):
                return result.get('text')

        except Exception as e:
            pass
    return []


if __name__ == '__main__':
    '''批量读取数据库上传'''
