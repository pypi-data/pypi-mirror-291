from .fits_image_reader import FITSImageReader

class FITSImage:
    def __init__(self, path=None):
        self.border_image = {}
        self.path = path
        self.data = None
        self.header = None
        self.data_relatif = None
        self.m = None
        self.s = None
        self.imgsub = {}
        self.aligned_image = {}
        if path is not None:
            FITSImageReader().read(self)
