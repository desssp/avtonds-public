from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from collections import defaultdict


def base_validation(cleaned_data):

    errors = defaultdict(str)

    def errors_add(attr_list, error_text):
        for a in attr_list:
            errors[a] += f'| {error_text} '

    def only_together_check_list_processing():
        only_together_check_list = [
            {
                'attr_list': ['user_type', 'full_name'],
                'error_text': 'Полное наименование для поставщиков и покупателей обязательно. '
                              'Для сотрудников - не заполняется',
            },
        ]

        for check in only_together_check_list:
            if [i for i in check['attr_list'] if not cleaned_data.get(i)] and [j for j in check['attr_list'] if cleaned_data.get(j)]:
                errors_add(check['attr_list'], check['error_text'])

    def only_one_of_check_list_processing():
        only_one_of_check_list = [
            # {
            #     'attr_list': ['user_type', 'is_staff'],
            #     'error_text': 'Сотрудник не может иметь тип клиента',
            # },
            {
                'attr_list': ['user_type', 'is_superuser'],
                'error_text': 'SuperUser не может иметь тип клиента',
            },
        ]

        for check in only_one_of_check_list:
            if len([i for i in check['attr_list'] if cleaned_data.get(i)]) > 1:
                errors_add(check['attr_list'], check['error_text'])

    def only_with_check_list_processing():
        only_with_check_list = [
            {
                'main_attr': 'is_superuser',
                'attr_list': ['is_staff'],
                'error_text': 'Суперпользователь должен иметь статус персонала',
            }
        ]

        for check in only_with_check_list:
            if cleaned_data.get(check['main_attr']) and [i for i in check['attr_list'] if not cleaned_data.get(i)]:
                errors_add(check['attr_list'], check['error_text'])

    only_together_check_list_processing()
    only_one_of_check_list_processing()
    only_with_check_list_processing()

    return errors


class DefaultUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'user_type', 'full_name', 'short_name', ]

    def _post_clean(self):
        super()._post_clean()
        for field, error in base_validation(self.cleaned_data).items():
            self.add_error(field, error)


class DefaultUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'short_name', ]

    def _post_clean(self):
        super()._post_clean()
        for field, error in base_validation(self.cleaned_data).items():
            self.add_error(field, error)
