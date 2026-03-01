from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter
def is_selected(value, arg):
    """Returns 'selected' if value matches arg."""
    return "selected" if str(value) == str(arg) else ""


@register.filter
def can_join(status):
    """Returns True if consultation status allows joining a session."""
    return status in ['scheduled', 'in_progress']
