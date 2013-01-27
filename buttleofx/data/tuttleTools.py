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
    # list of all Tuttle's plugins
    pluginCache = tuttle.core().getImageEffectPluginCache()
    plugins = pluginCache.getPlugins()

    # Creation of the dictionary
    pluginsIdentifiersAsDictionary = dict()
    for plugin in plugins:
        pluginId = plugin.getIdentifier()

        # We take the path of the plugin's parents (ex: 'tuttle/image/process/')
        fullPath = plugin.getDescriptor().getPluginGrouping()
        # We split this path to have a list of parents
        parentList = fullPath.split('/')

        # parentLabel is the parentPath of each element of this nex list of parents
        parentLabel = ""
        #pluginId = pluginId.lstrip('tuttle.')

        # We browse this list of parents
        for i in range(len(parentList)):
            # For each element, we want to create a new entry in the dictionary. So we update the parentLabel for this entry.
            parentLabel = parentLabel + parentList[i] + "/"

            # only if this parentLabel is not yet in the dictionary, we create a new list for this entry in the dictionary.
            if parentLabel not in pluginsIdentifiersAsDictionary:
                # if we are not yet at the end of the parentList, then we append the next parent
                if i < len(parentList) - 1:
                    pluginsIdentifiersAsDictionary[parentLabel] = []
                    pluginsIdentifiersAsDictionary[parentLabel].append(parentList[i + 1])
                # but if we are at the end of the parentList, then the child is the plugin itself, so we add its identifier.
                else:
                    pluginsIdentifiersAsDictionary[parentLabel] = []
                    pluginsIdentifiersAsDictionary[parentLabel].append(pluginId)
            # same reasoning, but here the parentLabel is already in the dictionary, we just append the child and not create a new list.
            else:
                if i < len(parentList) - 1:
                    if parentList[i + 1] not in pluginsIdentifiersAsDictionary[parentLabel]:
                        pluginsIdentifiersAsDictionary[parentLabel].append(parentList[i + 1])
                else:
                    if pluginId not in pluginsIdentifiersAsDictionary[parentLabel]:
                        pluginsIdentifiersAsDictionary[parentLabel].append(pluginId)
    # Here we are !
    return pluginsIdentifiersAsDictionary


def getPluginsIdentifiersByParentPath(parentPath):
    """
        Returns the list of what must be displayed in the application after clicking on "parentPath"
    """
    return getPluginsIdentifiersAsDictionary()[parentPath]
