from clipboard_processor.plugins._base import Plugin

try:
    import ulid
except ImportError:
    ulid = None


class UlidPlugin(Plugin):
    @classmethod
    def name(cls) -> str:
        return 'ulid'

    @classmethod
    def is_available(cls) -> bool:
        return ulid is not None

    def process(self, data: str) -> [str]:
        if len(data) != 26:
            return []
        try:
            u = ulid.ULID.from_str(data)
            return ['ULID at ' + u.datetime.isoformat().replace('+00:00', 'Z').replace('T', ' ')]
        except ValueError:
            return []

