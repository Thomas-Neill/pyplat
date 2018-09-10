class Vec:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    def __neg__(self):
        return Vec(-self.x,-self.y)
    def __add__(self,other):
        return Vec(self.x+other.x,self.y+other.y)
    def __sub__(self,other):
        return self + -other
    def __mul__(self,x):
        return Vec(self.x*x,self.y*x)
    def __truediv__(self,x):
        return self * (1/x)
    def __str__(self):
        return f"{self.x}i+{self.y}j"
    def __repr__(self):
        return f"Vec({self.x},{self.y})"
    def copy(self):
        return Vec(self.x,self.y)
