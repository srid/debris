# I keep utility and wrapper code here
# So simply do `from debris import foo' to use the feature `foo'

import os, cgi, sys
from google.appengine.ext.webapp import template as gae_template

TEMPLATE_GROUP = 'srid' # /templates/srid/
def template(response, name, values):
    """Render the given template to the `response' object"""
    # find templates in ../templates/
    path = os.path.join(os.path.dirname(__file__),
                        '..',
                        'templates',
                        TEMPLATE_GROUP,
                        name)
    response.out.write(gae_template.render(path, values))

def SHELL():
    """Break the application and run the PDB shell"""
    from pdb import Pdb
    Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__).set_trace(sys._getframe().f_back)

def form_to_db(request, model_instance):
    """Set table attributes from form values"""
    for key, field in model_instance.fields().items():
        value = cgi.escape(request.get(key))
        if value == "": # not available in form
            continue
        field_type = field.data_type
        if field_type is basestring:
            field_type = str # basestring cannot be initiated
        field_value = field_type(value)
        setattr(model_instance, key, field_value)

def rst2html(text):
    from docutils import core
    parts = core.publish_parts(text, writer_name='html4css1', settings_overrides={'_disable_config': True})
    return parts['fragment']
    
register = gae_template.create_template_register()
@register.filter
def rstify(text):
    return rst2html(text)
    
gae_template.register_template_library('debris') # this module itself
    