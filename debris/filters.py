# Django template filters

import re

from google.appengine.ext.webapp import template

from debris.html import rst2html


register =template.create_template_register()

@register.filter
def rstify(text):
    return rst2html(text)
    
display_tag_re = re.compile('([a-z])([A-Z])')
@register.filter
def display_tag(tag):
    """Display tag in readable way.
    Eg: display_tag("GoogleAppEngine") = "Google App Engine"
    """
    return display_tag_re.sub(r'\1 \2', tag)
    
@register.filter
def display_tags(tag_list):
    tags = []
    for tag in tag_list:
        tags.append('<a href="/tag/%s">%s</a>' % (tag, display_tag(tag)))
    return ', '.join(tags)
    
template.register_template_library('debris.filters') # this module itself
