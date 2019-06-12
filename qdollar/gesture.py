from qdollar.Point import Point
import math
class Gesture:
    Points = []
    name = ""
    SAMPLING_RESOLUTION = 32
    MAX_INT_COORDINATES = 1024
    LUT_SIZE = 64
    LUT_SCALE_FACTOR = MAX_INT_COORDINATES // LUT_SIZE
    LUT = [] #lookup table

    def __init__(self, name, points):
        self.name = name
        self.Points = points
        self.normalize()
        
    def normalize(self):
        self.Points = self.resample(self.Points, self.SAMPLING_RESOLUTION)
        self.Points = self.translate_to_origin(self.Points, self.SAMPLING_RESOLUTION)
        self.Points = self.scale(self.Points, self.LUT_SIZE)
        #self.transformCoordinatesToIntegers()
        self.LUT = self.compute_LUT(self.Points, self.SAMPLING_RESOLUTION, self.LUT_SIZE)
        #self.ConstructLUT()

    def resample(self, points, n):
        I = self.pathlength(points)/(n-1)
        D = 0
        newPoints = [points[0]]
        i = 1
        while True:
            if points[i].strokeId == points[i-1].strokeId:
                d = self.euclidean_distance(points[i-1],points[i])
                if D + d >= I:
                    x = points[i-1].x + ((I-D)/d) * (points[i].x - points[i-1].x)
                    y = points[i-1].y + ((I-D)/d) * (points[i].y - points[i-1].y)
                    q = Point(x,y,points[i].strokeId)
                    newPoints.append(q)
                    points.insert(i, q)
                    D = 0
                else:
                    D = D + d
            i += 1
            if i == len(points):
                break
        if len(newPoints) == n - 1:
            p = points[-1]
            newPoints.append(Point(p.x, p.y, p.strokeId))
        return newPoints
    
    def translate_to_origin(self, points, n):
        newpoints = []
        cx=0
        cy=0
        for point in points:
            cx = cx + point.x
            cy = cy + point.y
        cx = cx /n
        cy = cy/n
        for point in points:
            q = Point(point.x - cx, point.y - cy, point.strokeId)
            newpoints.append(q)
        return newpoints

    def scale(self, points, m):
        newPoints = []
        xmin = float('inf')
        xmax = float('-inf')
        ymin = float('inf')
        ymax = float('-inf')
        for p in points:
            xmin = min(xmin, p.x)
            ymin = min(ymin, p.y)
            xmax = max(xmax, p.x)
            ymax = max(ymax, p.y)
        s = max(xmax - xmin,ymax - ymin)/(m-1)
        for p in points:
            q = Point((p.x - xmin)/s, (p.y - ymin)/s, p.strokeId)
            q.intX = (p.x - xmin)//s
            q.intY = (p.y - ymin)//s
            newPoints.append(q)
        
        return newPoints

    def transformCoordinatesToIntegers(self):
        for p in self.Points:
            p.intX = int((p.x + 1.0) / 2.0 * (self.MAX_INT_COORDINATES - 1))
            p.intY = int((p.y + 1.0) / 2.0 * (self.MAX_INT_COORDINATES - 1))

    def compute_LUT(self, points, n , m):
        LUT = [[ 0 for x in range(m)] for y in range(m)]
        for x in range(m):
            for y in range(m):
                minimum = float('inf')
                index = -1
                for i in range(len(points)):
                    d = self.sqr_euclidean_distance(points[i], Point(x,y))
                    if d < minimum:
                        minimum = d
                        index = i
                LUT[x][y] = index
        return LUT

    def pathlength(self, points):
        d = 0
        for i in range(1,len(points)):
            if points[i].strokeId == points[i-1].strokeId:
                d = d + self.euclidean_distance(points[i-1], points[i])
        return d

    @staticmethod
    def sqr_euclidean_distance(a, b):
        return (a.x - b.x)**2 + (a.y - b.y)**2

    @staticmethod
    def euclidean_distance(a, b):
        return math.hypot(a.x - b.x, a.y - b.y)
    
    @staticmethod
    def printpoints(points):
        for p in points:
            print(p.x, p.y, p.strokeId, p.intX, p.intY)