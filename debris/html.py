# Functions related to HTML

import os
import cgi

from docutils import core
from google.appengine.ext.webapp import template as gae_template
from google.appengine.api        import users

import meta


def form_to_db(request, model_instance):
    """Copy the FORM values to the given entity properties (datastore model fields)
    """
    for key, field in model_instance.fields().items():
        value = request.get(key, default_value=None)
        
        field_type = field.data_type
        if field_type is basestring:
            field_type = str # basestring cannot be initiated
            
        # Skip fields that are not part of form (value == None), except in the
        # case of HTML checkbox where the corresponding form field in request.get
        # is 'absent by design' if the checkbox is unchecked
        # See http://code.google.com/appengine/docs/python/tools/webapp/requestdata.html
        # to understand how Google works around this HTML spec wart.
        if value == None and field_type is not bool:
            continue
        
        if value is not None:
            value = cgi.escape(value)
        
        # if __form_set_<key>__ is defined, use it instead of 'setattr'
        try:
            setter = getattr(model_instance, '__form_set_%s__' % key)
            field_value = value # need not to apply `field_type` as that will be done by the above custom setter
        except AttributeError:
            setter = lambda v: setattr(model_instance, key, v)
            field_value = field_type(value)
            
        setter(field_value)

def template(response, name, values):
    """Render the given template to the `response' object
    """
    # find templates in ../templates/
    path = os.path.join(os.path.dirname(__file__),
                        '..',
                        'templates',
                        meta.TEMPLATE_GROUP,
                        name)

    # Values common to all templates go here    
    values.update({
        'is_admin':    users.is_current_user_admin(),
        'login_url':   users.create_login_url("/"),
        'logout_url':  users.create_logout_url("/"),
        'site_title':  meta.SITE_TITLE,
    })
    
    if 'messages' not in values:
        values['messages'] = []
        
    # Testing warning (XXX: remove this once content is cleaned up at www.nearfar.org)
    values['messages'].append(
        "Please note that this site is a <b>test deployment environment</b> for " +
        "a software that I am currently writing. It will eventually become a place " +
        "for me to write; until then what you will see here is just random text."
    )
    
    response.out.write(gae_template.render(path, values))
    
def site_url(req, path=''):
    """Return the absolute site URL appending the `path' element if necessary
    """
    base_url = req.url[ : len(req.url) - len(req.path)]
    return base_url + '/' + path

def rst2html(text):
    """Convert reStructedText into a HTML fragment
    """
    parts = core.publish_parts(
        text,
        writer_name='html4css1',
        settings_overrides={
            '_disable_config': True,
            'embed_stylesheet': False,
            'stylesheet_path': 'data/html4css1/html4css1.css',
            'template': 'data/docutils/html4css1/template.txt',
            'initial_header_level': 3
        })
    return parts['fragment']
