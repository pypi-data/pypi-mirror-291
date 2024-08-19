import abc


class Output(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def name(cls):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def is_available(cls):
        raise NotImplementedError

    @abc.abstractmethod
    def show(self, title: str, content: str):
        raise NotImplementedError
