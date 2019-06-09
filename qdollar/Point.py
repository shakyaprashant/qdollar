class Point:
    strokeId = ""
    def __init__(self, x, y, strokeId=None):
        self.x = x
        self.y = y
        self.strokeId = strokeId
        self.intX = 0
        self.intY = 0