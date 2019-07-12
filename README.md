# qdollar

*qdollar* is a python implementation of the [$Q Super-Quick Recognizer](http://depts.washington.edu/ilab/proj/dollar/qdollar.html).
## About
>The $Q Super-Quick Recognizer is a 2-D gesture recognizer designed for rapid prototyping of gesture-based user interfaces, especially on low-power mobiles and wearables. It builds upon the $P Point-Cloud Recognizer but optimizes it to achieve a whopping 142× speedup, even while improving its accuracy slightly. $Q is currently the most performant recognizer in the $-family. Despite being incredibly fast, it is still fundamentally simple, easy to implement, and requires minimal lines of code. Like all members of the $-family, $Q is ideal for people wishing to add stroke-gesture recognition to their projects, now blazing fast even on low-capability devices.

## Installation
To install *qdollar* using pip
```
pip install qdollar
```

## Example
``` python
from qdollar.recognizer import Gesture,Recognizer, Point
t1 = [
    Point(0, 0, 1),
    Point(1, 1, 1),
    Point(0, 1, 2),
    Point(1, 0, 2)]
tmpl_1 = Gesture('X', t1)
tmpl_2 = Gesture('line', [
    Point(0, 0),
    Point(1, 0)])
templates = [ tmpl_1, tmpl_2]
gesture = Gesture('A',[Point( 31, 141, 1),Point(109, 222, 1),Point( 22, 219, 2),Point(113, 146, 2)])
res = Recognizer().classify(gesture, templates)
print(res[0].name)
```
