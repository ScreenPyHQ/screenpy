class Text(object):
    def viewed_by(self, the_actor):
        if self.multi_target is not None:
            texts = []
            for e in self.multi_target.resolve_all_for(the_actor):
                texts.append(e.text)

            return texts[0] if len(texts) == 1 else texts
        elif self.target is not None:
            return self.target.resolve_for(the_actor).text
        else:
            return None

    @staticmethod
    def of(target):
        return Text(target=target)

    @staticmethod
    def of_all(multi_target):
        return Text(multi_target=multi_target)

    def __init__(self, target=None, multi_target=None):
        self.target = target
        self.multi_target = multi_target
