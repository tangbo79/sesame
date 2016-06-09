from abc import ABCMeta

class Strategy:
    __metaclass__ = ABCMeta
    def decide(self, current_info):
        raise NotImplemented
