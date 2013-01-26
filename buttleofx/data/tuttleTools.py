from pyTuttle import tuttle


def getPlugins():
        """
            Returns the list of all Tuttle's plugins.
        """
        pluginCache = tuttle.core().getPluginCache()
        return pluginCache.getPlugins()


def getPluginsIdentifiers():
    """
        Returns the list of all names of Tuttle's plugins.
    """
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


def getPluginsIdentifiersAsDictionary():
    """
        Returns a dictionary of what we expect to see in the application when we want to create a node.
        Example :
        pluginsIdentifiersAsDictionary["tuttle/"] = ['image', 'param']
        pluginsIdentifiersAsDictionary["tuttle/image/"] = ['io', 'process', 'generator', 'display', 'tool']
        pluginsIdentifiersAsDictionary["tuttle/image/tool/"] = ['tuttle.dummy']
    """
    pluginCache = tuttle.core().getImageEffectPluginCache()
    plugins = pluginCache.getPlugins()

    pluginsIdentifiersAsDictionary = dict()
    for plugin in plugins:
        pluginId = plugin.getIdentifier()
        fullPath = plugin.getDescriptor().getPluginGrouping()
        parentList = fullPath.split('/')
        parentLabel = ""
        pluginId = pluginId.lstrip('tuttle.')
        for i in range(len(parentList)):
            parentLabel = parentLabel + parentList[i] + "/"
            if parentLabel not in pluginsIdentifiersAsDictionary:
                if i < len(parentList) - 1:
                    pluginsIdentifiersAsDictionary[parentLabel] = []
                    pluginsIdentifiersAsDictionary[parentLabel].append(parentList[i + 1])
                else:
                    pluginsIdentifiersAsDictionary[parentLabel] = []
                    pluginsIdentifiersAsDictionary[parentLabel].append(pluginId)
            else:
                if i < len(parentList) - 1:
                    if parentList[i + 1] not in pluginsIdentifiersAsDictionary[parentLabel]:
                        pluginsIdentifiersAsDictionary[parentLabel].append(parentList[i + 1])
                else:
                    if pluginId not in pluginsIdentifiersAsDictionary[parentLabel]:
                        pluginsIdentifiersAsDictionary[parentLabel].append(pluginId)
    return pluginsIdentifiersAsDictionary


def getPluginsIdentifiersByParentPath(parentPath):
    """
        Returns the list of what must be displayed in the application after clicking on "parentPath"
    """
    return getPluginsIdentifiersAsDictionary()[parentPath]
