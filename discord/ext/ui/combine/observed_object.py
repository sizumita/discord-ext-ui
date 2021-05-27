from .published import Published


class ObservedObject:
    def __init__(self):
        pass

    def __setattr__(self, key, value):
        if isinstance(getattr(self, key, None), Published):
            #  TODO viewの再描画
            if not isinstance(value, Published):
                return super(ObservedObject, self).__setattr__(key, Published(value))

        return super(ObservedObject, self).__setattr__(key, value)
