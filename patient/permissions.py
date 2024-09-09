from rest_framework.permissions import BasePermission


class IsInGroup(BasePermission):
    def __init__(self, group_name):
        self.group_name = group_name

    def has_permission(self, request, view):
        """ Смотрим есть ли в группах пользователя group_name (т.е принадлежит ли пользователь к группе droup_name)"""
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name=self.group_name).exists()


def get_permission_class(group_name):
    class Permission(IsInGroup):
        def __init__(self):
            super().__init__(group_name)
    return Permission
