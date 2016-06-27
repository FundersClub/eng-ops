def is_boolean(func):
    func.boolean = True
    return func


def short_description(desc):
    def inner(func):
        func.short_description = desc
        return func
    return inner
