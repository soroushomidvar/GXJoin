from Transformation.Blocks.RawPatternBlock import RawPatternBlock


class LiteralPatternBlock(RawPatternBlock):
    NAME = "LITERAL"

    def __init__(self, text=None):
        self._hash = None
        self.text = text

    def update_hash(self):
        self._hash = hash((self.NAME, self.text))


    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.update_hash()

    def apply(self, inp):
        return self.text

    @classmethod
    def extract(cls, inp, blk):
        s = set()
        s.add(LiteralPatternBlock(blk.text))
        return s

    def get_param_count(self):
        return 1

    @classmethod
    def get_param_space(cls, inp_lst):
        return {
            'text': inp_lst,
        }

    def __eq__(self, other):
        return self.text == other.text

    def __hash__(self):
        return self._hash

    def __repr__(self):
        return f"[LIT:'{self.text}'], "
