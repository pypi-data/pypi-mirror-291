class Container:
    def __init__(self):
        self._services = {}

    def register(self, interface, implementation):
        self._services[interface] = implementation

    def resolve(self, interface):
        return self._services[interface]
