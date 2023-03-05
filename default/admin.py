from django.contrib import admin
from .models import User, Request, Offer
from .forms import DefaultUserCreationForm, DefaultUserChangeForm
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe, SafeString
from django.urls import reverse
from django_admin_listfilter_dropdown.filters import RelatedOnlyDropdownFilter
from .filters import CarModelSimpleDropdownFilter


admin.site.site_header = "АвтоНДС"
admin.site.site_title = "Панель управления"
admin.site.index_title = "Добро пожаловать в панель управления АвтоНДС"


def get_filtered_fieldset(user, request):
    list_display_fields = [
        {'pos': False, 'name': 'user'},
        {'pos': True, 'name': 'status'},
        {'pos': True, 'name': 'button'}
    ]
    list_display = request.list_display

    for field in [f for f in list_display_fields if f['name'] not in list_display]:
        pos = list_display.__len__() if field['pos'] else 0
        list_display.insert(pos, field['name'])

    if not user.is_superuser:
        for field in [f['name'] for f in list_display_fields if f['name'] in list_display]:
            list_display.remove(field)

    return list_display


def get_filtered_readonly_fields(user, request, obj=None):
    list_readonly_fields = [
        {'only_for_superuser': False, 'only_insert': True, 'name': 'user'},
        {'only_for_superuser': True, 'only_insert': False, 'name': 'status'},
    ]
    readonly_fields = request.readonly_fields

    for field in [f['name'] for f in list_readonly_fields if f['name'] not in readonly_fields]:
        readonly_fields.insert(readonly_fields.__len__(), field)

    for field in [f for f in list_readonly_fields if f['name'] in readonly_fields]:
        if user.is_superuser and field['only_for_superuser']:
            readonly_fields.remove(field['name'])
        if field['only_insert'] and not obj:
            readonly_fields.remove(field['name'])
    return readonly_fields


def get_filtered_search_fields(user, request):
    search_fields = request.search_fields
    list_search_fields = ['user__full_name', 'user__short_name']

    for field in [f for f in list_search_fields if f not in search_fields]:
        search_fields.insert(search_fields.__len__(), field)
    if not user.is_superuser:
        for field in [f for f in list_search_fields if f in search_fields]:
            search_fields.remove(field)

    return search_fields


def get_user(user, obj, form):
    if not user.is_superuser:
        obj.user = user
    elif obj.user:
        pass
    elif form.cleaned_data['user']:
        obj.user = form.cleaned_data['user']
    return obj


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Custom user model main form"""
    add_form = DefaultUserCreationForm
    form = DefaultUserChangeForm

    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_type')}),
        (_('Имя'), {'fields': ('full_name', 'short_name')}),
        (_('Атрибуты'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Даты'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'full_name', 'short_name'),
        }),
    )
    list_display = ('email', 'full_name', 'short_name', 'is_staff')
    search_fields = ('email', 'full_name', 'short_name')
    ordering = ('email',)


class RequestAdmin(admin.ModelAdmin):
    # Поля, доступные для редактирования простым пользователям.
    user_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('car_mark', 'car_model', 'color', 'max_age', 'body_type', 'fuel', 'engine_capacity',
                       'engine_power', 'max_mileage', 'min_price', 'max_price', 'additional_requirements',
                       'status', ),
        }),
    )
    readonly_fields = ['status', 'created', 'last_update', ]
    list_display = ['user', 'car_mark', 'car_model', 'color', 'max_age', 'max_price', 'additional_requirements',
                    'status', 'button']  #
    # raw_id_list_displayfields = ('user',)
    search_fields = ['car_mark__name', 'car_model__name', 'user__full_name', 'user__short_name']
    list_filter = [('car_mark', RelatedOnlyDropdownFilter), CarModelSimpleDropdownFilter]
    # raw_id_fields = ['car_mark']

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj = get_user(request.user, obj, form)
            obj.save()

    def delete_model(self, request, obj):
        if not request.user.is_superuser:
            obj.status_id = 2
            obj.save()
        else:
            obj.delete()

    def preprocess_list_display(self, request):
        self.list_display = get_filtered_fieldset(request.user, self)

    def preprocess_readonly_fields(self, request, obj=None):
        self.readonly_fields = get_filtered_readonly_fields(request.user, self, obj)

    def preprocess_search_fields(self, request):
        self.search_fields = get_filtered_search_fields(request.user, self)

    def changelist_view(self, request, extra_context=None):
        self.preprocess_list_display(request)
        self.preprocess_search_fields(request)
        return super(RequestAdmin, self).changelist_view(request)

    def get_queryset(self, request):
        qs = super(RequestAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.prefetch_related('car_mark', 'car_model', 'status')
        else:
            return qs.filter(user=request.user).prefetch_related('car_mark', 'car_model', 'status')

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super(RequestAdmin, self).get_fieldsets(request, obj)
        return self.user_fieldsets

    def get_readonly_fields(self, request, obj=None):
        self.preprocess_readonly_fields(request, obj)
        if request.user.is_superuser:
            return super(RequestAdmin, self).get_readonly_fields(request, obj)
        return self.readonly_fields

    @staticmethod
    @admin.display(description='Операции')
    def button(obj) -> SafeString:
        url = f'{reverse("admin:default_offer_changelist")}?car_mark__id__exact={obj.car_mark_id}'
        return mark_safe(
            f'<a class="button" href="{url}">Искать предложения</a>')


class OfferAdmin(admin.ModelAdmin):
    # Поля, доступные для редактирования простым пользователям.
    user_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('car_mark', 'car_model', 'color', 'year_of_issue', 'body_type', 'fuel',
                       'engine_capacity', 'engine_power', 'mileage', 'price', 'location', 'additional_properties',
                       'status',),
        }),
    )
    readonly_fields = ['status', 'created', 'last_update', ]
    list_display = ['user', 'car_mark', 'car_model', 'color', 'year_of_issue', 'price',
                    'additional_properties', 'status', 'button']
    # raw_id_list_displayfields = ('user',)
    search_fields = ['car_mark__name', 'car_model__name', 'user__full_name', 'user__short_name']
    list_filter = [('car_mark', RelatedOnlyDropdownFilter), CarModelSimpleDropdownFilter]
    # list_select_related = ['car_mark', 'car_model', 'status']
    # raw_id_fields = ['car_mark', 'car_mark']

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj = get_user(request.user, obj, form)
            obj.save()

    def delete_model(self, request, obj):
        if not request.user.is_superuser:
            obj.status_id = 2
            obj.save()
        else:
            obj.delete()

    def preprocess_list_display(self, request):
        self.list_display = get_filtered_fieldset(request.user, self)

    def preprocess_readonly_fields(self, request, obj=None):
        self.readonly_fields = get_filtered_readonly_fields(request.user, self, obj)

    def preprocess_search_fields(self, request):
        self.search_fields = get_filtered_search_fields(request.user, self)

    def changelist_view(self, request, extra_context=None):
        self.preprocess_list_display(request)
        self.preprocess_search_fields(request)
        return super(OfferAdmin, self).changelist_view(request)

    def get_queryset(self, request):
        qs = super(OfferAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.prefetch_related('car_mark', 'car_model', 'status')
        else:
            return qs.filter(user=request.user).prefetch_related('car_mark', 'car_model', 'status')

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super(OfferAdmin, self).get_fieldsets(request, obj)
        return self.user_fieldsets

    def get_readonly_fields(self, request, obj=None):
        self.preprocess_readonly_fields(request, obj)
        if request.user.is_superuser:
            return super(OfferAdmin, self).get_readonly_fields(request, obj)
        return self.readonly_fields

    @staticmethod
    @admin.display(description='Операции')
    def button(obj) -> SafeString:
        url = f'{reverse("admin:default_request_changelist")}?car_mark__id__exact={obj.car_mark_id}'
        return mark_safe(
            f'<a class="button" href="{url}">Искать запросы</a>')
    button.short_description = 'Операции'


admin.site.register(Request, RequestAdmin)
admin.site.register(Offer, OfferAdmin)
