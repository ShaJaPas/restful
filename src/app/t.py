import traceback


class SomeObject(int):
    data = {"a": 1, "b": 3, "c": 5}

    def __init__(self):
        (_, _, _, text) = traceback.extract_stack()[-2]
        ret = self.data.get(text[: text.find("=")].strip())
        if ret:
            super().__init__()


a = SomeObject()
print(a)
print(dir(int))
