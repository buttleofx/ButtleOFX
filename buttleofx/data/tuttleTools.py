from pyTuttle import tuttle


def getPlugins():
        """
            Returns the list of all Tuttle's plugins.
        """
        pluginCache = tuttle.core().getPluginCache()
        return pluginCache.getPlugins()


def getPluginsNames():
    """
        Returns the list of all names of Tuttle's plugins.
    """
    return [plugin.getIdentifier() for plugin in getPlugins()]
    # not yet binded in python :
    #pluginCache = tuttle.core().getImageEffectPluginCache()
    #return [plugin.getDescriptor().getLabel() for plugin in pluginCache.getPlugins()]


def getPlugin(pluginName):
    """
        Returns a Tuttle's plugin thanks to its name (None if no plugin found).
    """
    for plugin in getPlugins():
        if(pluginName == plugin.getIdentifier()):
            return plugin
    return None
