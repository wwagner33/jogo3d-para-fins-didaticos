from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

class MouseCaptureApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # 1. Disable default camera mouse controls
        self.disableMouse()
        
        # 2. Configure window properties for capture
        props = WindowProperties()
        # props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(props)
        
        # 3. Add a task to read mouse movement every frame
        self.taskMgr.add(self.update_mouse, "UpdateMouseTask")

    def update_mouse(self, task):
        if self.mouseWatcherNode.hasMouse():
            # In Relative mode, (x, y) represents movement since last frame
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()
            
            btDireito = self.mouseWatcherNode.isButtonDown("mouse3")
            
            if btDireito:
                print("Botão direito do mouse pressionado!")
            
            # if x != 0 or y != 0:
            #    print(f"Mouse moved: X={x:.3f}, Y={y:.3f}")

        return task.cont

app = MouseCaptureApp()
app.run()
