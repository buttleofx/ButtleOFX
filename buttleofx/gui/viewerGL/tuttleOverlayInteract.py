from pyTuttle import tuttle


class TuttleOverlayInteract(tuttle.OverlayInteract):

    def __init__(self, glviewport, graph, node):
        print("TuttleOverlayInteract.__init__")
        print("TuttleOverlayInteract node:", node.asImageEffectNode())

        super(TuttleOverlayInteract, self).__init__(graph, node.asImageEffectNode())
        self.glviewport = glviewport

    def getViewportSize(self):
        print("TuttleOverlayInteract.getViewportSize")
        return (float(self.glviewport.width()), float(self.glviewport.height()))

    def getPixelScale(self):
        print("TuttleOverlayInteract.getPixelScale")
        scale = float(self.glviewport.getScale())
        return (scale, scale)

    def getBackgroundColour(self):
        print("TuttleOverlayInteract.getBackgroundColour")
        return (float(self.glviewport.getBgColor().red()),
                float(self.glviewport.getBgColor().green()),
                float(self.glviewport.getBgColor().blue()))

    def swapBuffers(self):
        print("ButtleOverlayInteract.swapBuffers")
        self.glviewport.swapBuffers()

    def redraw(self):
        print("ButtleOverlayInteract.redraw")
        self.glviewport.redraw()
