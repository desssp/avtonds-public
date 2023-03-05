from pathlib import Path
import os
import json
from collections import defaultdict
from default.models import CarMark, CarModel

file = os.path.join(os.path.join(os.path.dirname(__file__), 'sources'), 'cars.json')
with open(file, encoding='utf-8') as f:
    content = json.loads(f.read())


def get_attr_list():
    mark_attrs, models_attrs = list(), list()
    for item in content:
        for attr in item:
            if attr not in mark_attrs:
                mark_attrs.append(attr)
            if attr == 'models':
                for model in item[attr]:
                    for m_attr in model:
                        if m_attr not in models_attrs:
                            models_attrs.append(m_attr)
    print(mark_attrs)
    print(models_attrs)


def get_nullable_attrs(mark_attrs=None, models_attrs=None):
    mark_attrs = mark_attrs if mark_attrs else ['id', 'name', 'cyrillic-name', 'popular', 'country', 'models']
    models_attrs = models_attrs if models_attrs else ['id', 'name', 'cyrillic-name', 'class', 'year-from', 'year-to']
    result = defaultdict(list)
    marks, attrs = list(), list()
    for item in content:
        for mark_attr in [a for a in mark_attrs if a not in item]:
            result[item['id']].append(mark_attr)
        for model in item['models']:
            for models_attr in [a for a in models_attrs if a not in model or model[a] is None]:
                result[item['id']].append(f'model_{models_attr}')
    for r in result:
        marks.append(r)
        for attr in [a for a in result[r] if a not in attrs]:
            attrs.append(attr)
    print(marks)
    print('\n')
    print(attr)


def get_model_attrs(mark_id: str, model_id: str):
    for item in content:
        if item['id'] == mark_id:
            for attr in item:
                if attr != 'models':
                    print(f'{attr}: {item[attr]}')
            print('\n')
            for model in item['models']:
                if model['id'] == model_id:
                    for k in model:
                        print(f'{k}: {model[k]}')
                    print(model)
                    break
            break


def import_cars():
    for item in content:
        car_mark = CarMark(
            mark_char_id=item['id'],
            name=item['name'],
            name_cyrillic=item['cyrillic-name'],
            rating=item['popular'],
            country=item['country']
        )
        car_mark.save()
        for model in item['models']:
            car_model = CarModel(
                car_mark=car_mark,
                model_char_id=model['id'],
                name=model['name'],
                name_cyrillic=model['cyrillic-name'],
                model_class=model['class'],
                year_from=model['year-from'],
                year_to=model['year-to']
            )
            car_model.save()


def get_spaces():
    for item in content:
        mark = CarMark.objects.filter(mark_char_id=item['id']).first()
        if mark.id == 0 or not mark:
            print(item['id'])
# get_nullable_attrs()
# get_model_attrs('BUFORI', 'GENEVA')
# get_attr_list()
# import_cars()
get_spaces()
