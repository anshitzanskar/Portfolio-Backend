#Not needed as of now, just a sample file

import logging
import subprocess
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger= logging.getLogger(__name__)

SERVER_LIST= []
COLO_PATH= '/home/zanskar/titan_data/portfolios'

def run_cmds(cmds):
    for cmd in cmds:
        process = subprocess.Popen(cmd, shell=True)
        if process.wait()!=0:
            logger.warning(f"Error in cmd:{cmd},   {str(process.wait())}")
            raise Exception(cmd + ", code:"+ str(process.wait()))

def rsync_commands() -> list:
    commands= []
    for server in SERVER_LIST:
        command = f'rsync -azvP {server}:{COLO_PATH}/* {Path.home()}/Portfolio-Backend/portfolios/.'
        commands.append(command)
    return commands

if __name__ == '__main__':
    rsync_command_list= rsync_commands()

    run_cmds(rsync_command_list)
