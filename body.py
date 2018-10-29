from vec import Vec
class Body:
    def __init__(self,rect):
        self.rect = rect
        self.v = Vec()
        self.x_old = self.rect.pos.x
        self.y_old = self.rect.pos.y
        self.linked_body = None # A body to move when this body moves, in the same direction
    def update(self,dt):
        self.rect.pos += self.v*dt
        if self.linked_body != None:
            self.linked_body.rect.pos += self.v*dt
            self.linked_body = None
    def begin_update(self):
        self.x_old = self.rect.pos.x
        self.y_old = self.rect.pos.y
    def reset_x(self):
        self.rect.pos.x = self.x_old
    def reset_y(self):
        self.rect.pos.y = self.y_old
    def update_x(self,dt):
        self.rect.pos.x += self.v.x*dt
    def update_y(self,dt):
        self.rect.pos.y += self.v.y*dt
    def update_with_v(self,v,dt):
        self.rect.pos += v*dt
