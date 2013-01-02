from pyTuttle import tuttle

class ButtleOverlayInteract(tuttle.OverlayInteract):
    def __init__(self, node):
        super(ButtleOverlayInteract, self).__init__(node)
        #tuttle.OverlayInteract.__init__(self, node)
    
    def getViewportSize( self, outWidth, outHeight ):
        outWidth = 123.
        outHeight = 123.

    def getPixelScale( self, outXScale, outYScale ):
        outXScale = 1.
        outYScale = 1.
        
    def getBackgroundColour( self, outR, outG, outB ):
        outR = 1.
        outG = 1.
        outB = 1.

    def swapBuffers(self):
        print("ButtleOverlayInteract.swapBuffers")

    def redraw(self):
        print("ButtleOverlayInteract.redraw")
