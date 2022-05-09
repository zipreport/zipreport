import base64
import json
from pathlib import Path
from typing import Union
from uuid import uuid4

import markupsafe
from jinja2 import pass_environment
from jinja2.defaults import DEFAULT_FILTERS

from zipreport.template.jinjaloader import JinjaReportLoader
from zipreport.misc import html_tag

# attribute names
ARG_DATA = 'data'
ATTR_SRC = 'src'
ATTR_ALT = 'alt'
ATTR_WIDTH = 'width'
ATTR_HEIGHT = 'height'
ATTR_CLASS = 'class'

# named parameters allowed in image filters
IMAGE_NAMED_PARAMS = [ARG_DATA, ATTR_ALT, ATTR_WIDTH, ATTR_HEIGHT, ATTR_CLASS]


def dynamic_image(args: list, kwargs: Union[dict, None], extension: str):
    """
    Dynamic Image tag generator
    possible args: [Environment, generator, data, alt, width, height, class]
    :param args: argument list
    :param kwargs: named argument list
    :param extension: generated file extension
    """
    al = len(args)
    if al < 2:
        raise RuntimeError("Invalid number of arguments")

    # load & validate env and callable
    loader = args[0].loader
    generator = args[1]
    callable_generator = callable(generator)

    if not isinstance(loader, JinjaReportLoader):
        raise RuntimeError("Invalid environment. png() filter requires ReportLoader")

    if not callable_generator and not isinstance(generator, str):
        raise RuntimeError("png() must be applied to a callable function or a placeholder string")

    # process args and kwargs
    if kwargs is None:
        kwargs = {}

    img_args = {}
    ai = 2  # user arguments start in 3
    for arg in IMAGE_NAMED_PARAMS:
        if arg in kwargs.keys():
            img_args[arg] = kwargs[arg]
        else:
            if ai < al:
                img_args[arg] = args[ai]
        ai += 1

    # callable may not always require data
    if ARG_DATA not in img_args.keys():
        img_args[ARG_DATA] = None

    # execute callable & save image
    zpt = loader.get_report()
    if callable_generator:
        result = generator(img_args[ARG_DATA])
        name = Path('data') / (uuid4().hex + extension)
        zpt.add(name, result)
    else:
        # if generator is string, skip image generation and use specified file
        name = generator

    # assemble html tag
    img_args.pop(ARG_DATA)
    img_args[ATTR_SRC] = "{}".format(name)
    return markupsafe.Markup(html_tag('img', img_args))


@pass_environment
def dynamic_png(*args, **kwargs) -> markupsafe.Markup:
    """
    Dynamic PNG img tag generator
    Can be called either via positional arguments or via named arguments, or both

    Positional args:
        {{ callable | png(data_source, alt_text, width, height, css_class }}

    Named args:
        {{ callable | png(data=data_source, alt=alt_text, width=width, height=height, class=css_class= }}

    Mixed args:
        {{ callable | png(with=128, height=128 }}
    """
    return dynamic_image(args, kwargs, '.png')


@pass_environment
def dynamic_gif(*args, **kwargs) -> markupsafe.Markup:
    """
    Dynamic GIF img tag generator
    Can be called either via positional arguments or via named arguments, or both

    Positional args:
        {{ callable | gif(data_source, alt_text, width, height, css_class }}

    Named args:
        {{ callable | gif(data=data_source, alt=alt_text, width=width, height=height, class=css_class= }}

    Mixed args:
        {{ callable | gif(with=128, height=128 }}
    """
    return dynamic_image(args, kwargs, '.gif')


@pass_environment
def dynamic_jpg(*args, **kwargs) -> markupsafe.Markup:
    """
    Dynamic JPG img tag generator
    Can be called either via positional arguments or via named arguments, or both

    Positional args:
        {{ callable | jpg(data_source, alt_text, width, height, css_class }}

    Named args:
        {{ callable | jpg(data=data_source, alt=alt_text, width=width, height=height, class=css_class= }}

    Mixed args:
        {{ callable | jpg(with=128, height=128 }}
    """
    return dynamic_image(args, kwargs, '.jpg')


@pass_environment
def dynamic_svg(*args, **kwargs) -> markupsafe.Markup:
    """
    Dynamic SVG img tag generator
    Can be called either via positional arguments or via named arguments, or both

    Positional args:
        {{ callable | svg(data_source, alt_text, width, height, css_class }}

    Named args:
        {{ callable | svg(data=data_source, alt=alt_text, width=width, height=height, class=css_class= }}

    Mixed args:
        {{ callable | svg(with=128, height=128 }}
    """
    return dynamic_image(args, kwargs, '.svg')


def do_json(*args) -> markupsafe.Markup:
    if len(*args) != 1:
        raise RuntimeError("Invalid number of arguments. json filter requires a variable")
    try:
        return markupsafe.Markup(json.dumps(args[0]))
    except ValueError:
        raise


# Register filters
DEFAULT_FILTERS['png'] = dynamic_png
DEFAULT_FILTERS['gif'] = dynamic_gif
DEFAULT_FILTERS['jpg'] = dynamic_jpg
DEFAULT_FILTERS['svg'] = dynamic_svg
DEFAULT_FILTERS['json'] = do_json
