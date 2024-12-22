from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """Проверка на наличие пользователя user в группе group_name"""
    if group_name == 'no_group':  # Проверяем, состоит ли пользователь в какой-либо группе
        return not user.groups.all()
    return user.groups.filter(name=group_name).exists()
