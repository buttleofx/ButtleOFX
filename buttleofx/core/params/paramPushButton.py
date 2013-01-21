class ParamPushButton(object):

    def __init__(self, label, trigger, enabled=True, text="Default"):
        self.paramType = "ParamPushButton"
        self.label = label
        self.trigger = trigger
        self.enabled = enabled
        self.text = text
