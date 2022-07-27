from typing import Dict


class LibCalBorg:
    _shared_state: Dict[str, str] = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class LibCalCache(LibCalBorg):
    def __init__(self, current):
        super().__init__()
        self.current = current
