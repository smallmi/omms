#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''


import six


def check_perms(request, perm, raise_exception=False):
    user = request.user
    if isinstance(perm, six.string_types):
        perms = (perm, )
    else:
        perms = perm
    # First check if the user has the permission (even anon users)
    if user.has_perms(perms):
        return True
    # In case the 403 handler should be called raise the exception
    if raise_exception:
        # raise PermissionDenied
        return False