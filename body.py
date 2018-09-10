from vec import Vec
class Body:
    def __init__(self,rect):
        self.rect = rect
        self.v = Vec()
        self.x_old = self.rect.pos.x
        self.y_old = self.rect.pos.y
    def update(self):
        self.rect.pos += self.v/60
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
