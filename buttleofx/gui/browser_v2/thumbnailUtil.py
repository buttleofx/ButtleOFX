import os
from pyTuttle import tuttle
from multiprocessing.pool import ThreadPool


class ThumbnailUtil:
    """
    Helper class used to link buttle with tuttle for thumbnail functions
    """
    def __init__(self):
        tuttle.core().preload(False)
        self._thumbnailCache = tuttle.ThumbnailDiskCache()
        self._thumbnailCache.setRootDir(os.path.join(tuttle.core().getPreferences().getTuttleHomeStr(), "thumbnails_cache"))

    def getThumbnail(self, id):
        return self._thumbnailCache.getThumbnail(id)

    def getThumbnailPath(self, id):
        return self._thumbnailCache.getThumbnailPath(id)


# Concentrates in one point every compute process for thumbnail:
# Limits the thread and processes used for thumbnail processes
thumbnailPool = ThreadPool(processes=2)
