from vec import Vec
class Rect:
    def __init__(self,pos,w,h):
        self.pos = pos
        self.w = w
        self.h = h
    def show(self):
        return (self.pos.x,500-int(self.pos.y)-self.h,self.w,self.h)
    def copy(self):
        return Rect(self.pos.copy(),self.w,self.h)
    def points(self):
        return [Vec(self.pos.x,self.pos.y),Vec(self.pos.x+self.w-1,self.pos.y),Vec(self.pos.x,self.pos.y+self.h-1),Vec(self.pos.x+self.w-1,self.pos.y+self.h-1)]
    def contains(self,point):
        return (self.pos.x <= point.x < self.pos.x+self.w-1) and (self.pos.y <= point.y < self.pos.y+self.h-1)
    def collides(self,other):
        if self == other:
            return False
        for i in self.points():
            if other.contains(i):
                return True
        for i in other.points():
            if self.contains(i):
                return True
        return False
    def center(self):
        return Vec(self.pos.x + self.w//2,self.pos.y + self.h//2)
