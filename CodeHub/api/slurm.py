import os
import subprocess
import pandas as pd
from datetime import datetime
from flask import abort, Flask, abort, request, jsonify, render_template

app = Flask(__name__)


## sinfo
def py_sinfo():
    output_format = request.args.get("format")
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

    if output_format == "table":
        return render_template("../template/table.html",
                               table=sinfo.to_html(index=True))
    elif output_format == "json":
        return sinfo.to_json()
    else:
        return abort(404)


def py_job(username):
    startdate = request.args.get("startdate", None)
    enddate = request.args.get("enddate", None)
    status = request.args.get("status", None)
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

    return render_template("../template/table.html",
                           table=pd_sjob.to_html(index=True))
    #return pd_sjob.to_json()


if __name__ == '__main__':
    '''
  sinfo = py_sinfo()
  print("sinfo:\n", sinfo)
  sjob = ("sjob", py_job("terencelau"))
  print("your tasks/jobs:\n", sjob)
  '''
    #app.run()
    app.run(host="0.0.0.0", port=8076, debug=True)
