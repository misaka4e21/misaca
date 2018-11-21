from django.conf import settings

def local_user_ap_id(username, domain=""):
    if not domain or domain=="":
        domain = settings.MISACA_FEDERATION_DOMAIN
    return "https://%s/users/%s" % (domain, username)

def user_ap_id(user):
    if user.is_local:
        return local_user_ap_id(user.username, user.domain)
    else:
        return user.uri

def local_user_box_uri(user, boxname):
    return "%s/%s" % (user_ap_id(user), boxname)

def user_box_uri(user, boxname):
    try:
      box_url = getattr(user, "%s_url" % (boxname,))
      if box_url and box_url != '':
          return box_url
    finally:
      return local_user_box_uri(user, boxname)

def user_url(user):
    if user.url:
        return user.url
    else:
        return "https://%s/@%s" % (settings.MISACA_FEDERATION_DOMAIN, user.username)
    
