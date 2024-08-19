class YCClass1:
    Count = 0
    def __init__(self):
        YCClass1.Count += 1
        self.Count = YCClass1.Count
    def __str__(self):
        return ('YCClass1 ' + str(self.Count))


