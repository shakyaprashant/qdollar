from qdollar.gesture import Gesture, Point
import math
class Recognizer:

    def classify(self, gesture, templates):
        n = 32
        m = 64
        score = float('inf')
        for template in templates:
            d = self.cloud_match(gesture, template, n, score)
            if d < score:
                score = d
                result = template
        return (result, score)
    
    def cloud_match(self, gesture, template, n, minimum):
        step = math.floor(n**0.5)
        #compute lower bounds for both matching directions between points and template
        LB1 = self.compute_lower_bound(gesture.Points, template.Points, step, template.LUT, n)
        LB2 = self.compute_lower_bound(gesture.Points, template.Points, step, gesture.LUT, n)
        indexLB = 0
        for i in range(0,n,step):
            if LB1[indexLB] < minimum:
                minimum = min(minimum, self.cloud_distance(gesture.Points, template.Points, n, i, minimum))
            if LB2[indexLB] < minimum:
                minimum = min(minimum, self.cloud_distance(template.Points, gesture.Points, n, i, minimum))
            indexLB = indexLB+1
        return minimum

    def cloud_distance(self, points, template, n, start, minSoFar):
        unmatched = [i for i in range(0,n)]
        i = start
        weight = n
        sum = 0
        index = -1
        indexunmatched = 0
        while True:
            minimum = float('inf')
            for j in range(indexunmatched,n):
                d = Gesture.sqr_euclidean_distance(points[i], template[j])
                if d < minimum:
                    minimum = d
                    index = j
            #print("index = ",index)
            unmatched[index] = unmatched[indexunmatched]
            sum = sum + (weight*minimum)
            if sum >= minSoFar:
                return sum
            weight = weight - 1
            i = (i + 1)%n
            indexunmatched+=1
            if i == start:
                break
        return sum
    
    def compute_lower_bound(self, points, template, step, LUT, n):
        LB = [0 for i in range((n//step) + 1)]
        SAT = [0 for i in range(n)]

        LB[0] = 0
        for i in range(n):
            index = LUT[int(points[i].intX)][int(points[i].intY)]
            d = Gesture.sqr_euclidean_distance(points[i], template[index])
            if i == 0:
                SAT[i] = d
            else:
                SAT[i] = SAT[i-1] + d
            LB[0] = LB[0] + (n-i)*d
        index = 1
        for i in range(step,n,step):
            LB[index] = LB[0] + i*SAT[n-1] - n*SAT[i-1]
            index+=1
        return LB