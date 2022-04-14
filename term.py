#!/usr/bin/env python

import sys
from easyterm import easyterm

command = sys.argv[1:]
if(command[0] == '--'):
    command = command[1:]

easyterm.EasyTermLib(
    command=command,
)
