import bottle
from urllib.parse import urljoin


def path(url=None, view=None, name=None):
    if not url:
        raise ValueError('Path needs an url')
    if not view:
        raise ValueError('Path needs a view')

    if not url.startswith('/'):
        url = urljoin('/', url)

    bottle.route(
        path=url,
        method=view.methods,
        callback=view().callback,
        name=name
    )
