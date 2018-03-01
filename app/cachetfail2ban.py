#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import jsonschema
import re
import time
import subprocess
from conf import schema
from jsonschema import validate
from clize import clize, run
import cachetclient.cachet as cachet


jaillist_pattern = re.compile('.*- Jail list:\s*(.+)')
jailstatus_pattern = re.compile('.*- Currently banned:\s*(\d+)')

def log(msg):
    print('{} {}'.format(time.strftime('%y-%m-%d %H:%M:%S'), msg))

def collect_status(conf):

    metrics = cachet.Metrics(
        endpoint=conf['api_url'], api_token=conf['api_token'])
    json_metrics = json.loads(metrics.get())

    # dict where key is id and value is component struct
    metric_dict = dict()
    for metric in json_metrics['data']:
        metric['processed'] = False
        metric_dict[metric['name']] = metric

    # retrieve list of jails
    jail_list = []
    output = str(subprocess.check_output(
        ['fail2ban-client', 'status'], universal_newlines=True))
    for line in output.splitlines():
        r = re.match(jaillist_pattern, line)
        if r:
            jail_list = [token.strip() for token in r.group(1).split(',')]

    # retrieve jail status
    for jail in jail_list:
        output = str(subprocess.check_output(
            ['fail2ban-client', 'status', jail], universal_newlines=True))
        for line in output.splitlines():
            r = re.match(jailstatus_pattern, line)
            if r:
                metric_name = 'fail2ban-' + jail
                if metric_name in metric_dict:
                    metric_dict[metric_name]['processed'] = True
                    metric_dict[metric_name]['newvalue'] = int(r.group(1))
                    log('collect jail {} => {}'.format(jail, r.group(1)))

    # send updates to cachet API
    points = cachet.Points(
        endpoint=conf['api_url'], api_token=conf['api_token'])

    now = time.strftime('%Y-%m-%d %H:%M:%S')
    for metric in metric_dict.values():
        if metric['processed']:
            points.post(id=metric['id'], value=metric['newvalue'], created_at=now, updated_at=now)
            log('post point {} at {} ({})'.format(metric['newvalue'], now, metric))


def load_json(filename):
    jsondoc = None
    with open(filename, 'rt') as json_file:
        jsondoc = json.loads(json_file.read())
    return jsondoc


@clize
def cachet_fail2ban(config_pathname):

    # load and validate startup config
    conf = load_json(config_pathname)
    json_schema = json.loads(schema.json_schema)
    validate(conf, json_schema)

    collect_status(conf)


if __name__ == '__main__':
    run(cachet_fail2ban)
