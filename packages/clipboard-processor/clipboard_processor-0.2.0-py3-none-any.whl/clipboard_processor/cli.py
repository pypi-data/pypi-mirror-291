import argparse
import logging
import sys
import time

from clipboard_processor.input import PyperclipInput, XclipPrimaryInput
from clipboard_processor.output import NotifyOutput, StdoutOutput
from clipboard_processor.output.ui import UiOutput
from clipboard_processor.plugins import *
from clipboard_processor.plugins.hex import HexPlugin
from clipboard_processor.plugins.oui import OuiPlugin

INPUTS = [
    PyperclipInput,
    XclipPrimaryInput,
]

PLUGINS = [
    AwsAccountIdPlugin,
    Base64Plugin,
    HexPlugin,
    JwtPlugin,
    OuiPlugin,
    UlidPlugin,
    UnixTimePlugin,
    VinPlugin,
]

OUTPUTS = [
    NotifyOutput,
    StdoutOutput,
    UiOutput,
]

logger = logging.getLogger(__name__)

_BLUE = '\033[94m'
_GREEN = '\033[92m'
_GRAY = '\033[90m'
_RESET = '\033[0m'


def main():
    available_plugin_names = [p.name() for p in PLUGINS if p.is_available()]
    available_input_names = [i.name() for i in INPUTS if i.is_available()]
    available_output_names = [o.name() for o in OUTPUTS if o.is_available()]

    if not available_plugin_names:
        print('No plugins available. Please check README and install dependencies if needed. Exiting.')
        sys.exit(1)

    if not available_input_names:
        print('No input methods available. Please check README and install dependencies if needed. Exiting.')
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Automatic clipboard processor')
    parser.add_argument('-p', '--plugin', action='append',
                        help='Process clipboard data with specific plugin. '
                             'If no plugin is specified, all available plugins will be used.',
                        choices=available_plugin_names, default=[])
    parser.add_argument('-i', '--input', action='store', help='Select input method',
                        choices=available_input_names, default=available_input_names[0])
    parser.add_argument('-o', '--output', action='append', help='Select output method. Defaults to stdout',
                        choices=available_output_names)
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format='%(message)s')

    if len(args.plugin) == 0:
        active_plugins = [p() for p in PLUGINS if p.name() in available_plugin_names]
    else:
        active_plugins = [p() for p in PLUGINS if p.name() in args.plugin]

    outputs = [o() for o in OUTPUTS if o.name() in (args.output or ['ui'])]
    input_ = [i for i in INPUTS if i.name() == args.input][0]()

    last_value = None
    while True:
        try:
            current_value = input_.read()
            if last_value is None:
                last_value = current_value
            elif current_value != last_value:
                last_value = current_value
                if current_value.strip() == '':
                    continue
                logger.debug(f'{_GRAY}Processing: "{_BLUE}{current_value}{_GRAY}"{_RESET}')
                results = []
                for plugin in active_plugins:
                    results_from_plugin = plugin.process(current_value)
                    if results_from_plugin:
                        logger.debug(f'{_GRAY}Result from {_GREEN}{plugin.name()}{_GRAY}:{_RESET}')
                        for result in results_from_plugin:
                            logger.debug(f'{_BLUE}{result}{_RESET}')

                    results.extend(results_from_plugin)

                if results:
                    title = _trim(current_value, max_length=50)
                    content = '\n'.join(results)
                    for output in outputs:
                        output.show(title, content)

            time.sleep(0.1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.warning('Error occurred during processing', exc_info=e)


def _trim(s: str, max_length: int) -> str:
    return s[:max_length] + ('...' if len(s) > max_length else '')
