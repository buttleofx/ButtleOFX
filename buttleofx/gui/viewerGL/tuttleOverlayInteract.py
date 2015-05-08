import logging

from pyTuttle import tuttle


class TuttleOverlayInteract(tuttle.OverlayInteract):

    def __init__(self, glviewport, graph, node):
        logging.debug("TuttleOverlayInteract.__init__")
        logging.debug("TuttleOverlayInteract node:", node.asImageEffectNode())

        super(TuttleOverlayInteract, self).__init__(graph, node.asImageEffectNode())
        self.glviewport = glviewport

    def getViewportSize(self):
        logging.debug("TuttleOverlayInteract.getViewportSize")
        return (float(self.glviewport.width()), float(self.glviewport.height()))

    def getPixelScale(self):
        logging.debug("TuttleOverlayInteract.getPixelScale")
        scale = float(self.glviewport.getScale())
        return (scale, scale)

    def getBackgroundColour(self):
        logging.debug("TuttleOverlayInteract.getBackgroundColour")
        return (float(self.glviewport.getBgColor().red()),
                float(self.glviewport.getBgColor().green()),
                float(self.glviewport.getBgColor().blue()))

    def swapBuffers(self):
        logging.debug("ButtleOverlayInteract.swapBuffers")
        self.glviewport.swapBuffers()

    def redraw(self):
        logging.debug("ButtleOverlayInteract.redraw")
        self.glviewport.redraw()
