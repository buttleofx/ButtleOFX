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
    #pluginCache = tuttle.core().getImageEffectPluginCache()
    #return [plugin.getDescriptor().getLabel() for plugin in pluginCache.getPlugins()]
    pluginCache = tuttle.core().getPluginCache()
    return [plugin.getIdentifier() for plugin in pluginCache.getPlugins()]

def getPlugin(pluginName):
    """
        Returns a Tuttle's plugin thanks to its name (None if no plugin found).
    """
    for plugin in getPlugins():
        if(pluginName == plugin.getIdentifier()):
            return plugin
    return None

