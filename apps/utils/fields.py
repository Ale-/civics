from django.forms.models import ModelChoiceIterator, ModelChoiceField
from itertools import groupby


class Grouped(object):
    """Auxiliar object to create hierarchical options in a select.
       See https://djangosnippets.org/snippets/1968/"""

    def __init__(self, queryset, group_by_field,
                 group_label=None, *args, **kwargs):
        """
        ``group_by_field`` is the name of a field on the model to use as
                           an optgroup.
        ``group_label`` is a function to return a label for each optgroup.
        """
        super(Grouped, self).__init__(queryset, *args, **kwargs)
        self.group_by_field = group_by_field
        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)


class GroupedModelChoiceIterator(ModelChoiceIterator):
    """An interator that returns model information in a way that is groupable in a select.
       See https://djangosnippets.org/snippets/1968/"""

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset.all()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, choices in groupby(self.queryset.all(),
                    key=lambda row: getattr(row, self.field.group_by_field)):
            if self.field.group_label(group):
                yield (
                    self.field.group_label(group),
                    [self.choice(ch) for ch in choices]
                )


class GroupedModelChoiceField(Grouped, ModelChoiceField):
    """A field to display a ModelChoiceField in a select with optgroups.
       See https://djangosnippets.org/snippets/1968/"""

    choices = property(Grouped._get_choices, ModelChoiceField._set_choices)
