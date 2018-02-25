#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import re
import subprocess

jaillist_pattern = re.compile('.*- Jail list:\s*(.+)')
jailstatus_pattern = re.compile('.*- Currently banned:\s*(\d+)')


def collect_status(config):

    # retrieve list of jails
    jail_list = []
    output = str(subprocess.check_output(
        ['cat', 'fail2ban-client_status.txt'], universal_newlines=True))
    for line in output.splitlines():
        r = re.match(jaillist_pattern, line)
        if r:
            jail_list = [token.strip() for token in r.group(1).split(',')]

    # retrieve jail status
    for jail in jail_list:
        output = str(subprocess.check_output(
            ['cat', 'fail2ban-client_status_sshd.txt'], universal_newlines=True))
        for line in output.splitlines():
            r = re.match(jailstatus_pattern, line)
            if r:
                print('Jail {} : {}'.format(jail, r.group(1)))


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
