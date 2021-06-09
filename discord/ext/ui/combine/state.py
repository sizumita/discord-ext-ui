from ..view import View


def state(name: str):
    def getter(instance):
        return instance.__dict__[name]

    def setter(instance, value):
        instance.__dict__[name] = value
        if isinstance(instance, View):
            instance.update_sync()

    return property(getter, setter)
