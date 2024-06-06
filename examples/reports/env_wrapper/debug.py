# ZipReport Custom Jinja2 Enviroment Wrapper
# This is a stub file to aid zipreport debug by providing custom filter initialization
#
# To use the MyCustomWrapper class with zipreport debug:
#
# $ zipreport debug --wrapper debug.MyCustomWrapper  custom_filter_example/
#
import markupsafe
from jinja2 import pass_environment, Environment

from zipreport.template import EnvironmentWrapper


@pass_environment
def defoxifier(*args, **kwargs) -> markupsafe.Markup:
    """
    Example filter that replaces "fox" with "racoon"
    """
    al = len(args)
    if al < 2:
        raise RuntimeError("Invalid number of arguments")

    text = args[1].replace("fox", "racoon")
    return markupsafe.Markup(text)


class MyCustomWrapper(EnvironmentWrapper):
    def wrap(self, e: Environment):
        # register our fancy defoxifier filter
        e.filters["defoxifier"] = defoxifier
        return e
