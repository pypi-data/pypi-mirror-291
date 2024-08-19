class YCClass:
    Count = 0
    def __init__(self):
        YCClass.Count += 1
        self.Count = YCClass.Count
    def __str__(self):
        return ('YCClass ' + str(self.Count))
    def __del__(self):
        YCClass.Count -= 1

if __name__ == '__main__':
    yc1 = YCClass()
    print(yc1)
    yc2 = YCClass()
    print(yc2)
    del yc2
    yc3 = YCClass()
    print(yc3)
    print(dir(yc1))
