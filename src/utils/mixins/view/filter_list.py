from django.http import Http404
from django.utils.translation import gettext as _
from django.views.generic.list import ListView


class FilterListView(ListView):
    def get(self, request, *args, **kwargs):
        pks = kwargs.get("pks")
        if pks is not None:
            pk_list = self._parse_pk_list(pks)
            self.object_list = self.model._default_manager.filter(pk__in=pk_list)
        else:
            self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {"class_name": self.__class__.__name__}
                )
        context = self.get_context_data()
        return self.render_to_response(context)

    @staticmethod
    def _parse_pk_list(pk_list: str) -> list[str]:
        return eval(pk_list)
