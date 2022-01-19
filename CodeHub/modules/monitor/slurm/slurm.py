import os
import subprocess
import pandas as pd
from datetime import datetime


## sinfo
def py_sinfo() -> dict:
    sinfo = subprocess.run(["sinfo", "-l"],
                           stdout=subprocess.PIPE)  ## binary string
    # print(sinfo.stdout.decode("ascii"))
    sinfo = sinfo.stdout.decode("ascii").split("\n")
    time = sinfo[0]
    out_length = len(sinfo[:-1])
    pd_sinfo = []

    for i in range(1, out_length):
        pd_sinfo.append(sinfo[i].split())

    pd_sinfo = pd.DataFrame(pd_sinfo)
    header = pd_sinfo.iloc[0]
    sinfo = pd.DataFrame(pd_sinfo.values[1:], columns=header)
    return sinfo.to_dict()
"""
example data
{'PARTITION': {0: 'CPU-Compute*', 1: 'GPU-Compute', 2: 'GPU-Compute'}, 'AVAIL': {0: 'up', 1: 'up', 2: 'up'}, 'TIMELIMIT': {0: '7-00:00:00', 1: '7-00:00:00', 2: '7-00:00:00'}, 'JOB_SIZE': {0: '1-infinite', 1: '1-infinite', 2: '1-infinite'}, 'ROOT': {0: 'no', 1: 'no', 2: 'no'}, 'OVERSUBS': {0: 'NO', 1: 'NO', 2: 'NO'}, 'GROUPS': {0: 'all', 1: 'all', 2: 'all'}, 'NODES': {0: '2', 1: '1', 2: '1'}, 'STATE': {0: 'idle', 1: 'mixed', 2: 'idle'}, 'NODELIST': {0: 'Compute[2030005000-2030005001]', 1: 'Compute2030005002', 2: 'Compute2030005003'}}
"""


def py_sacct(username:str, startdate:str, enddate:str) -> dict:
    startdate = datetime.strptime(startdate, "%Y-%m-%d").strftime("%Y-%m-%d")
    enddate = datetime.strptime(enddate, "%Y-%m-%d").strftime("%Y-%m-%d")
    #sjob = subprocess.run(["sacct","-u", "{}".format(username)], stdout = subprocess.PIPE)
    sjob = subprocess.run([
        "sacct", "-u", "{}".format(username), "-S", "{}".format(startdate),
        "-E", "{}".format(enddate)],
                            stdout=subprocess.PIPE)
    # getpass.getuser() -> get username from bash (import getpass)
    sjob = sjob.stdout.decode("ascii").split("\n")
    out_length = (sjob[:-1])
    pd_sjob = []
    for i in range(0, len(out_length)):
        pd_sjob.append(sjob[i].split())

    pd_sjob = pd.DataFrame(pd_sjob)
    header = pd_sjob.iloc[0]
    pd_sjob = pd_sjob[2:]
    pd_sjob.columns= header
    return pd_sjob.to_dict()

"""
example data
{'JobID': {2: '1300', 3: '1300.0', 4: '1301', 5: '1301.0', 6: '1302', 7: '1302.0', 8: '1303', 9: '1303.batch', 10: '1304', 11: '1305', 12: '1306', 13: '1306.0', 14: '1307', 15: '1307.0', 16: '1308', 17: '1308.0', 18: '1309', 19: '1309.0'}, 'JobName': {2: 'sh', 3: 'bash', 4: 'sh', 5: 'bash', 6: 'sh', 7: 'bash', 8: 'run.sh', 9: 'batch', 10: 'sh', 11: 'sh', 12: 'sh', 13: 'bash', 14: 'sh', 15: 'bash', 16: 'sh', 17: 'bash', 18: 'sh', 19: 'bash'}, 'Partition': {2: 'CPU-Compu+', 3: 'stat', 4: 'GPU-Compu+', 5: 'stat', 6: 'GPU-Compu+', 7: 'stat', 8: 'CPU-Compu+', 9: 'stat', 10: 'GPU-Compu+', 11: 'GPU-Compu+', 12: 'GPU-Compu+', 13: 'stat', 14: 'GPU-Compu+', 15: 'stat', 16: 'GPU-Compu+', 17: 'stat', 18: 'GPU-Compu+', 19: 'stat'}, 'Account': {2: 'stat', 3: '1', 4: 'stat', 5: '1', 6: 'stat', 7: '1', 8: 'stat', 9: '4', 10: 'stat', 11: 'stat', 12: 'stat', 13: '1', 14: 'stat', 15: '1', 16: 'stat', 17: '1', 18: 'stat', 19: '1'}, 'AllocCPUS': {2: '1', 3: 'COMPLETED', 4: '1', 5: 'FAILED', 6: '1', 7: 'CANCELLED', 8: '4', 9: 'CANCELLED', 10: '1', 11: '1', 12: '1', 13: 'CANCELLED', 14: '1', 15: 'FAILED', 16: '1', 17: 'COMPLETED', 18: '1', 19: 'CANCELLED'}, 'State': {2: 'COMPLETED', 3: '0:0', 4: 'FAILED', 5: '1:0', 6: 'COMPLETED', 7: '0:9', 8: 'TIMEOUT', 9: '0:15', 10: 'CANCELLED+', 11: 'CANCELLED+', 12: 'CANCELLED+', 13: '0:9', 14: 'FAILED', 15: '127:0', 16: 'COMPLETED', 17: '0:0', 18: 'COMPLETED', 19: '0:9'}, 'ExitCode': {2: '0:0', 3: None, 4: '1:0', 5: None, 6: '0:0', 7: None, 8: '0:0', 9: None, 10: '0:0', 11: '0:0', 12: '0:0', 13: None, 14: '127:0', 15: None, 16: '0:0', 17: None, 18: '0:0', 19: None}}
"""

def py_squeue(username:str=None) -> dict:
    if username == None:
        squeue = subprocess.run(["squeue"], stdout=subprocess.PIPE)
    else:
        squeue = subprocess.run(["squeue", "--user", "{}".format(username)], stdout=subprocess.PIPE)
    squeue = squeue.stdout.decode("ascii").split("\n")
    out_length = (squeue[:-1])
    pd_squeue = []
    for i in range(0, len(out_length)):
        pd_squeue.append(squeue[i].split())
    pd_squeue = pd.DataFrame(pd_squeue)
    header = pd_squeue.iloc[0]
    pd_squeue = pd.DataFrame(pd_squeue.values[1:], columns=header)
    return pd_squeue.to_dict()

"""
example data
{'JOBID': {0: '4079'}, 'PARTITION': {0: 'GPU-Compu'}, 'NAME': {0: 'gpu-test'}, 'USER': {0: 'duxinwei'}, 'ST': {0: 'R'}, 'TIME': {0: '11:23'}, 'NODES': {0: '1'}, 'NODELIST(REASON)': {0: 'Compute2030005002'}}
"""
