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
        Returns a dictionary of what we need to display the menu of the node creation.
        For each level in the menu we need to have the list of items of the submenu
        When the items are plugins, we need to know their label to display, and their identifier to be able to create the node.
        So this dictionary returns a tuple :
            - if it's a plugin, the tuple is : (pluginLabel, pluginIdentifier)
            - if i's a category of plugins, the tuple is : (categoryLabel, "")
        The keys of this dictionary are the "paths" of each element of the menu.
        Example :
        pluginsIdentifiersAsDictionary["buttle/tuttle/"] = ['image', 'param']
        pluginsIdentifiersAsDictionary["buttle/tuttle/image/"] = ['io', 'process', 'generator', 'display', 'tool']
        pluginsIdentifiersAsDictionary["buttle/tuttle/image/tool/"] = ['tuttle.dummy']
    """

    # root label : parent of all plugins
    buttleLabel = "buttle/"

    # list of all Tuttle's plugins
    pluginCache = tuttle.core().getImageEffectPluginCache()
    plugins = pluginCache.getPlugins()

    print("nb plugins:", len(plugins))
    # Creation of the dictionary
    pluginsIdentifiersAsDictionary = dict()

    # if no plugin found we just add the "buttle" key with a message for the user
    if len(plugins) == 0:
        pluginsIdentifiersAsDictionary[buttleLabel] = []
        pluginsIdentifiersAsDictionary[buttleLabel].append(('Error : no plugin found...', False))
        return pluginsIdentifiersAsDictionary

    for plugin in plugins:
        pluginId = plugin.getIdentifier()
        # All plugin labels in Tuttle are preceded by 'Tuttle', so we can delete 'Tuttle' from the beginning of the word. It doesn't affect other plugins, not preceded by 'Tuttle'.
        pluginLabel = plugin.getDescriptor().getLabel().replace('Tuttle', '', 1)

        # We take the path of the plugin's parents (ex: 'tuttle/image/process/')
        fullPath = plugin.getDescriptor().getPluginGrouping()
        # We split this path to have a list of parents
        parentList = None
        if fullPath.startswith(' '):
            parentList = fullPath[1:].split(' ')
        else:
            parentList = fullPath.split('/')

        # parentLabel is the parentPath of each element of this nex list of parents
        parentLabel = buttleLabel

        # We browse this list of parents. For each element, we want to create a new entry in the dictionary.
        for i in range(len(parentList) + 1):

            # only if this parentLabel is not yet in the dictionary, we create a new list for this entry in the dictionary.
            if parentLabel not in pluginsIdentifiersAsDictionary:
                # if we are not yet at the end of the parentList, then we append the next parent
                if i < len(parentList):
                    pluginsIdentifiersAsDictionary[parentLabel] = []
                    pluginsIdentifiersAsDictionary[parentLabel].append((parentList[i], ""))
                # but if we are at the end of the parentList, then the child is the plugin itself, so we add its identifier.
                else:
                    pluginsIdentifiersAsDictionary[parentLabel] = []
                    pluginsIdentifiersAsDictionary[parentLabel].append((pluginLabel, pluginId))
            # same reasoning, but here the parentLabel is already in the dictionary, we just append the child and not create a new list.
            else:
                if i < len(parentList):
                    if parentList[i] not in [p[0] for p in pluginsIdentifiersAsDictionary[parentLabel]]:
                        pluginsIdentifiersAsDictionary[parentLabel].append((parentList[i], ""))
                else:
                    if pluginId not in [p[1] for p in pluginsIdentifiersAsDictionary[parentLabel]]:
                        pluginsIdentifiersAsDictionary[parentLabel].append((pluginLabel, pluginId))
            # We have created the right entry for this element, and we want to create a new one at the next iteration. So we update the parentLabel for this entry.
            if i < len(parentList):
                parentLabel = parentLabel + parentList[i] + "/"
    # Here we are !
    return pluginsIdentifiersAsDictionary


def getPluginsIdentifiersByParentPath(parentPath):
    """
        Returns the list of what must be displayed in the application after clicking on "parentPath"
    """
    return getPluginsIdentifiersAsDictionary()[parentPath]
