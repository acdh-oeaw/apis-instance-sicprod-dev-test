from itertools import chain
from django import template
from django.forms import model_to_dict

register = template.Library()

@register.inclusion_tag("model_to_table.html")
def model_to_table(instance):
    opts = instance._meta
    data = {}

    exclude = getattr(instance, "detailviewexclude", [])

    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if f.name in exclude:
            continue
        if getattr(f, "editable", False):
            fname = f"detailview_{f.name}"
            key = getattr(f, "verbose_name", f.name)
            if hasattr(instance, fname) and callable(getattr(instance, fname)):
                data[key] = getattr(instance, fname)()
            else:
                data[key] = f.value_from_object(instance) # getattr(instance, f.name)

    return {
            "model": data,
    }
