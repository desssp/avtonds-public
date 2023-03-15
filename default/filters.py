from django_admin_listfilter_dropdown.filters import SimpleDropdownFilter
from .models import CarModel


class CarModelSimpleDropdownFilter(SimpleDropdownFilter):
    title = 'Модель'
    parameter_name = 'car_model'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        car_mark_id = request.GET.get('car_mark__id__exact') or request.GET.get('car_mark')

        if car_mark_id:
            entity_list = model_admin.get_queryset(request).filter(car_mark=car_mark_id)
        else:
            entity_list = model_admin.get_queryset(request)

        lookup_options = (
            (entity.car_model.id, entity.car_model.name) for entity in entity_list
        )
        return lookup_options

    def queryset(self, request, queryset):
        car_model_id = self.value()
        if car_model_id:
            car_mark_id = request.GET.get('car_mark__id__exact') or request.GET.get('car_mark')
            if car_mark_id and int(car_mark_id) == CarModel.objects.get(id=car_model_id).car_mark_id:
                return queryset.filter(car_model=car_model_id)
        return queryset
