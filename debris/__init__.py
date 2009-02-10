# I keep utility and wrapper code here
# So simply do `from debris import foo' to use the feature `foo'

import os, cgi, sys, logging
from google.appengine.ext.webapp import template as gae_template
from google.appengine.api import users

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

def admin_only(handler_method):
    """Decorator to restrict a method to be run by site administrator only"""
    def check_login(self, *args, **kwargs):
        user = users.get_current_user()
        is_admin = users.is_current_user_admin()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        elif is_admin:
            handler_method(self, *args, **kwargs)
        else:
            self.error(403)
    return check_login
