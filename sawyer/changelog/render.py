from jinja2 import Environment, PackageLoader


def render_changelog(context, template='default.md'):
    env = Environment(loader=PackageLoader('sawyer', 'templates'))
    template = env.get_template(template)

    return template.render(**context)
