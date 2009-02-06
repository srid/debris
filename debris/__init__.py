# I keep utility and wrapper code here
# So simply do `from debris import foo' to use the feature `foo'

import os, cgi, sys
from google.appengine.ext.webapp import template as gae_template


def template(response, name, values):
    """Render the given template to the `response' object"""
    # find templates in ../templates/
    path = os.path.join(os.path.dirname(__file__),
                        '..',
                        'templates',
                        name)
    response.out.write(gae_template.render(path, values))

def SHELL():
    """Break the application and run the PDB shell"""
    import pdb
    debugger = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)
    debugger.set_trace(sys._getframe().f_back)

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

class formed:
    
    def __init__(self, request):
        self.request = request
        
    def get(self, key):
        return cgi.escape(self.request.get(key))
