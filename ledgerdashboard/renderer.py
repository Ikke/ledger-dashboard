import pystache
from os.path import abspath, dirname, join, exists


class PartialLoader:
    def __init__(self, partial_path):
        self.partials = {}
        self.partial_path = partial_path

    def get(self, name):
        if name in self.partials:
            return self.partials[name]
        else:
            return self.load_partial(name)

    def load_partial(self, partial_name):
        partial_path = join(self.partial_path, partial_name.replace('_', '/') + ".mustache")
        if exists(partial_path):
            with open(partial_path) as f:
                return f.read()
        else:
            return None


class LayoutRenderer():
    def __init__(self):
        pass

    def render(self, context):
        template_path = join(dirname(abspath(__file__)), "templates")
        loader = PartialLoader(partial_path=join(template_path, 'partials'))

        loader.partials['content'] = loader.load_partial(context.__class__.__name__.lower())

        return pystache.Renderer(search_dirs=template_path, partials=loader).render_name('layout', context)

