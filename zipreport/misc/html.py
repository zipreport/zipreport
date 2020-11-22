from html import escape


def html_tag(name, params: dict, content=None):
    """
    HTML tag helper
    Generated format: <name params>content</name> or <name params />
    :param name:
    :param params:
    :param content:
    :return: html tag built from the parameters
    """

    properties = []
    for k, v in params.items():
        if v is not None:
            if type(v) is str:
                v = '"{}"'.format(escape(v))
            properties.append("=".join([k, str(v)]))
    if content is None:
        return "<{} {} />".format(name, " ".join(properties))
    return "<{} {}>{}</{}>".format(name, " ".join(properties), content, name)
