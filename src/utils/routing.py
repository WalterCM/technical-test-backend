import bottle
from urllib.parse import urljoin


def path(url=None, view=None, name=None):
    if not url:
        raise ValueError('Path needs an url')
    if not view:
        raise ValueError('Path needs a view')

    if not url.startswith('/'):
        url = urljoin('/', url)

    for method in view.methods:
        bottle.route(
            path=url,
            method=method,
            callback=getattr(view(), method.lower()),
            name=name
        )
