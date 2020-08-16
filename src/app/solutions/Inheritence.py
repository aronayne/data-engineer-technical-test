import json

class class1():
    def __init__(self, attribute1):
        self.attribute1 = attribute1

class class2(class1):
    def __init__(self, attribute2):
        class1.__init__(self, 'test')
        self.attribute2 = attribute2

c1 = class1('c1')
c2 = class2(c1)

print(json.dumps(c2.__dict__))


