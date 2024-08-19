from clipboard_processor.plugins._base import Plugin
from datetime import datetime, tzinfo, timezone


class UnixTimePlugin(Plugin):
    @classmethod
    def name(cls) -> str:
        return 'unixtime'

    @classmethod
    def is_available(cls) -> bool:
        return True

    def process(self, data: str) -> [str]:
        if len(data) in [10, 13, 16]:
            try:
                timestamp = int(data)
                timestamp_s = None
                if len(str(data)) == 10:
                    timestamp_s = timestamp
                elif len(str(data)) == 13:
                    timestamp_s = timestamp / 1000
                elif len(str(data)) == 16:
                    timestamp_s = timestamp / 1000000
                return [datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
                        .isoformat()
                        .replace('+00:00', 'Z')
                        .replace('T', ' ')]
            except ValueError as e:
                pass
        return []
