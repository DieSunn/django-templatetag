from django import template
from django.urls import reverse, NoReverseMatch
from menu.models import MenuItem

register = template.Library()

@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    # 1. Получаем все пункты меню одним запросом (Requirement: 1 запрос к БД)
    menu_items = MenuItem.objects.filter(name=menu_name).select_related('parent')
    
    # Получаем текущий URL из request
    request = context.get('request')
    current_path = request.path if request else ''

    # 2. Преобразуем QuerySet в список словарей для удобной мутации
    # и сразу вычисляем реальные URL
    items_dict = {}
    for item in menu_items:
        try:
            if item.named_url:
                url = reverse(item.named_url)
            else:
                url = item.url
        except NoReverseMatch:
            url = item.url
            
        items_dict[item.id] = {
            'id': item.id,
            'title': item.title,
            'parent_id': item.parent_id,
            'url': url,
            'children': [],
            'is_active': False,
            'is_expanded': False
        }

    # 3. Строим дерево и ищем активный элемент
    root_items = []
    active_item_id = None

    for item_id, item in items_dict.items():
        if item['url'] == current_path:
            item['is_active'] = True
            active_item_id = item_id

        if item['parent_id']:
            if item['parent_id'] in items_dict:
                items_dict[item['parent_id']]['children'].append(item)
        else:
            root_items.append(item)

    # 4. Раскрываем дерево для активного элемента
    
    if active_item_id:
        current_id = active_item_id
        while current_id:
            item = items_dict[current_id]
            item['is_expanded'] = True
            current_id = item['parent_id']
    
    return {'menu_items': root_items}