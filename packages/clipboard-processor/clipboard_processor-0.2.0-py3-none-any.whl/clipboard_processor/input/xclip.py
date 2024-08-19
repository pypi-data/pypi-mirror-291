import shutil
import subprocess

from clipboard_processor.input._base import Input


class XclipPrimaryInput(Input):
    @classmethod
    def name(cls):
        return 'xclip-primary'

    @classmethod
    def is_available(cls):
        return shutil.which('xclip') is not None

    def read(self) -> str:
        return subprocess.check_output(['xclip', '-o', '-selection', 'primary']).decode('utf-8')
