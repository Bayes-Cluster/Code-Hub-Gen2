from distutils.log import Log
import jwt
import datetime

from functools import wraps

from modules.dashboard import blueprint
from modules.authentication.models import Users

from flask import request
from flask import redirect, url_for, session
from flask import Flask, jsonify, render_template, make_response
from modules.config import secret_key, exp_time

from modules.utils.token import *
from modules.config import secret_key, exp_time

from modules.monitor.plot import plot


@blueprint.route("/dashboard")
@token_renew
@token_required
@check_token_revoke
def dashboard(token):
    token = token
    username = request.cookies.get('username')
    data = dict({'PARTITION': {0: 'CPU-Compute*', 1: 'GPU-Compute', 2: 'GPU-Compute'}, 'AVAIL': {0: 'up', 1: 'up', 2: 'up'}, 'TIMELIMIT': {0: '7-00:00:00', 1: '7-00:00:00', 2: '7-00:00:00'}, 'JOB_SIZE': {0: '1-infinite', 1: '1-infinite', 2: '1-infinite'}, 'ROOT': {0: 'no', 1: 'no', 2: 'no'}, 'OVERSUBS': {0: 'NO', 1: 'NO', 2: 'NO'}, 'GROUPS': {0: 'all', 1: 'all', 2: 'all'}, 'NODES': {0: '2', 1: '1', 2: '1'}, 'STATE': {0: 'idle', 1: 'mixed', 2: 'idle'}, 'NODELIST': {0: 'Compute[2030005000-2030005001]', 1: 'Compute2030005002', 2: 'Compute2030005003'}})
    script, div = plot(data)
    return render_template('main/dashboard.html', name=username, token=request.args["token"], script1=script, div1=div)

# TODO: Add bokeh dashboard

@blueprint.route("/dashboard/slurm")
@token_renew
@token_required
@check_token_revoke
def slurm_status(token):
    token = token
    username = request.cookies.get('username')
    data = dict({'PARTITION': {0: 'CPU-Compute*', 1: 'GPU-Compute', 2: 'GPU-Compute'}, 'AVAIL': {0: 'up', 1: 'up', 2: 'up'}, 'TIMELIMIT': {0: '7-00:00:00', 1: '7-00:00:00', 2: '7-00:00:00'}, 'JOB_SIZE': {0: '1-infinite', 1: '1-infinite', 2: '1-infinite'}, 'ROOT': {0: 'no', 1: 'no', 2: 'no'}, 'OVERSUBS': {0: 'NO', 1: 'NO', 2: 'NO'}, 'GROUPS': {0: 'all', 1: 'all', 2: 'all'}, 'NODES': {0: '2', 1: '1', 2: '1'}, 'STATE': {0: 'idle', 1: 'mixed', 2: 'idle'}, 'NODELIST': {0: 'Compute[2030005000-2030005001]', 1: 'Compute2030005002', 2: 'Compute2030005003'}})
    script, div = plot(data)
    return render_template('main/slurm.html', name=username, token=request.args["token"], script1=script, div1=div)

    