from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
"""
    获取用户session中的信息并返回
"""

def get_user_from_session(view_func):
    def wrapper(request, *args, **kwargs):
        # 从会话中获取用户信息
        is_login = request.session.get('is_login')
        session_username = request.session.get("username")
        session_phone = request.session.get("phone")
        session_role = request.session.get("role")
        session_pic = request.session.get("pic")
        session_list = [is_login, session_username, session_phone, session_role, session_pic]
        # 将用户信息作为参数传递给视图函数
        return view_func(request, session_list=session_list,*args, **kwargs)
    return wrapper


def has_permission(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            user_groups = Group.objects.filter(users=request.user)  # 获取用户所属的权限组
            user_permissions = set()  # 用于存储用户所具有的权限索引
            for group in user_groups:
                rules = group.rules.split(',')  # 将权限组的rules字段拆分成索引列表
                user_permissions.update(rules)  # 将权限索引添加到用户权限集合中
            requested_url = request.path_info  # 获取请求的路由地址
            if requested_url in user_permissions:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("你没有访问这个页面的权限！")
        else:
            return HttpResponse("Please log in to access this page.")
    return login_required(_wrapped_view)
