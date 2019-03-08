class Number(object):
    def viewed_by(self, the_actor):
        return len(self.target.resolve_all_for(the_actor))

    @staticmethod
    def of(target):
        return Number(target=target)

    def __init__(self, target=None, multi_target=None):
        self.target = target
