from pyTuttle import tuttle

class TuttleOverlayInteract(tuttle.OverlayInteract):
    def __init__(self, glviewport, graph, node):
        print("TuttleOverlayInteract.__init__")
        print("TuttleOverlayInteract node:", node.asImageEffectNode())
        super(TuttleOverlayInteract, self).__init__(graph, node.asImageEffectNode())
        self.glviewport = glviewport
    
    def getViewportSize( self, outWidth, outHeight ):
        print("TuttleOverlayInteract.getViewportSize")
        outWidth = float(self.glviewport.width())
        outHeight = float(self.glviewport.height())

    def getPixelScale( self, outXScale, outYScale ):
        print("TuttleOverlayInteract.getPixelScale")
        outXScale = float(self.glviewport.getScale())
        outYScale = outXScale
        
    def getBackgroundColour( self, outR, outG, outB ):
        print("TuttleOverlayInteract.getBackgroundColour")
        outR = float(self.glviewport.getBgColor().red())
        outG = float(self.glviewport.getBgColor().green())
        outB = float(self.glviewport.getBgColor().blue())

    def swapBuffers(self):
        print("ButtleOverlayInteract.swapBuffers")
        self.glviewport.swapBuffers()

    def redraw(self):
        print("ButtleOverlayInteract.redraw")
        self.glviewport.redraw()
