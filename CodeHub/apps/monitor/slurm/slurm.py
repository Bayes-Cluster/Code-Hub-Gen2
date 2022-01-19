import os
import subprocess
import pandas as pd
from datetime import datetime


## sinfo
def py_sinfo() -> pd.DataFrame:
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
    return sinfo


def py_sacct(username:str, startdate:str, enddate:str) -> pd.DataFrame:
    startdate = datetime.strptime(startdate, "%Y%m%d").strftime("%Y-%m-%d")
    enddate = datetime.strptime(enddate, "%Y%m%d").strftime("%Y-%m-%d")
    #sjob = subprocess.run(["sacct","-u", "{}".format(username)], stdout = subprocess.PIPE)
    sjob = subprocess.run([
        "sacct", "-u", "{}".format(username), "-S", "{}".format(startdate),
        "-E", "{}".format(enddate), "--state", "{}".format(status)
    ],
                          stdout=subprocess.PIPE)
    # getpass.getuser() -> get username from bash (import getpass)
    sjob = sjob.stdout.decode("ascii").split("\n")
    out_length = (sjob[:-1])
    pd_sjob = []
    for i in range(0, len(out_length)):
        pd_sjob.append(sjob[i].split())

    pd_sjob = pd.DataFrame(pd_sjob)
    header = pd_sjob.iloc[0]
    pd_sjob = pd.DataFrame(pd_sjob.values[1:], columns=header)
    return pd_sjob.to_json()

def py_squeue(username:str=None):
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
    return pd_squeue.to_json()

