import base64
from pathlib import Path
from uuid import uuid4

import markupsafe
from jinja2 import environmentfilter, contextfilter
from jinja2.defaults import DEFAULT_FILTERS

from zipreport.jinja2.loader import ReportLoader
from zipreport.misc import RoOptionalList, html_tag


@environmentfilter
def placeholder(*args, **kwargs):
    """
    """
    loader = args[0].loader
    if not isinstance(loader, ReportLoader):
        raise RuntimeError("Invalid environment. Placeholder filter requires ReportLoader")
    zpt = loader.get_report()
    print(zpt.get_fs().list(''))
    data = args[1]
    print(args)
    return "|".join(zpt.get_fs().list(''))

@environmentfilter
def do_dynamic_png(*args, **kwargs):
    """
    """
    loader = args[0].loader
    generator = args[1]
    if len(args) < 4:
        raise RuntimeError("png() requires 2 mandatory arguments: (datasource, alt_name)")

    if not isinstance(loader, ReportLoader):
        raise RuntimeError("Invalid environment. png() filter requires ReportLoader")

    if not callable(generator):
        raise RuntimeError("png() must be applied to a callable variable")

    data = args[2]
    args = RoOptionalList(args[3:])
    width = args.get(1, 100)
    height = args.get(2, 100)

    zpt = loader.get_report()
    result = generator(data)
    name = Path('data') / (uuid4().hex + '.png')
    zpt.add(name, result)

    return markupsafe.Markup(html_tag('img',{
        'src': "{}".format(name),
        'alt': args.get(0),
        'width': width,
        'height': height,
        'class': args.get(3),
    }))


DEFAULT_FILTERS['placeholder'] = placeholder
DEFAULT_FILTERS['png'] = do_dynamic_png
