import hashlib
import json
import sys

from .mysql_client import mc

def load_boss_jobids(data_source):
    jobSet = set()
    res = mc.get_job_item(data_source)
    for v in res:
        md5 = v.get("json_md5")
        jobSet.add(md5)
    return jobSet

def load_boss_jobids_v2(data_source):
    jobSet = set()
    res = mc.get_job_item(data_source)
    for v in res:
        job_id = v.get("job_id")
        jobSet.add(job_id)
    return jobSet

def get_md5_str(data):
    jd = json.dumps(data)
    jd_md5 = hashlib.md5(jd.encode(encoding='UTF-8')).hexdigest()
    return jd_md5

def signal_handler(signal, frame):
    print ('\nSignal Catched! You have just type Ctrl+C!')
    sys.exit(0)