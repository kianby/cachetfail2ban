#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import re
import subprocess

output = str(subprocess.check_output(
            ['cat', 'fail2ban-client_status.txt'], universal_newlines=True))
for line in output.splitlines():
    print(line)
