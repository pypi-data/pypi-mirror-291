import signal
import subprocess
import time

from test_cli import SLEEP_STARTUP_SECONDS, BASE64_DATA, SLEEP_PROCESSING_SECONDS, BASE64_DECODED
from util import run_cli


def test_cli_with_xclip_primary():
    # given
    subprocess.run(['xclip', '-selection', 'primary'], input='', encoding='utf-8', check=True)

    # when
    with run_cli('--input', 'xclip-primary', '--output', 'stdout') as proc:
        time.sleep(SLEEP_STARTUP_SECONDS)
        subprocess.run(['xclip', '-selection', 'primary'], input=BASE64_DATA, encoding='utf-8', check=True)
        time.sleep(SLEEP_PROCESSING_SECONDS)
        proc.send_signal(signal.SIGINT)

        output = proc.stdout.readlines()

    # then
    assert proc.returncode == 0
    assert BASE64_DATA in output[0]
    assert output[1].strip() == BASE64_DECODED
