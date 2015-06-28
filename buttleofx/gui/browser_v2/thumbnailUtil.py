import os
from pyTuttle import tuttle


class ThumbnailUtil:
    def __init__(self):
        tuttle.core().preload(False)
        self._thumbnailCache = tuttle.ThumbnailDiskCache()
        self._thumbnailCache.setRootDir(os.path.join(tuttle.core().getPreferences().getTuttleHomeStr(), "thumbnails_cache"))

    def getThumbnail(self, id):
        return self._thumbnailCache.getThumbnail(id)

    def getThumbnailPath(self, id):
        return self._thumbnailCache.getThumbnailPath(id)
