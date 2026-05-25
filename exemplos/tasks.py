from direct.showbase.ShowBase import ShowBase
from direct.task import Task

class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)        # Load multiple objects
        self.obj1 = self.loader.loadModel("../models/box")
        self.obj1.reparentTo(render)
        self.obj1.setPos(-2, 0, 0)

        self.obj2 = self.loader.loadModel("models/box")
        self.obj2.reparentTo(render)
        self.obj2.setPos(2, 0, 0)

        # Add independent tasks for each object
        self.taskMgr.add(self.move_object1, "MoveObj1Task")
        self.taskMgr.add(self.move_object2, "MoveObj2Task")

    def move_object1(self, task):
        # Rotate object 1
        self.obj1.setH(self.obj1.getH() + 1)
        return Task.cont

    def move_object2(self, task):
        # Move object 2 back and forth
        import math
        self.obj2.setX(math.sin(task.time) * 2)
        return Task.cont

game = MyGame()
game.run()