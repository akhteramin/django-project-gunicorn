from django import template
import time
# from ipaypos.settings import APP_LIST, APP_URL

register = template.Library()

# @register.filter
# def get_app_name(value, arg):
#     # timestamp = "2008-09-26T01:51:42.000Z"
#     print("value")
#     print(value)
#     app_name=''
#     try:
#         app_name = APP_LIST[str(value)]
#     except Exception as e:
#         return app_name
#     return app_name
#
# @register.filter
# def get_app_url(value, arg):
#     # timestamp = "2008-09-26T01:51:42.000Z"
#     app_url=''
#     try:
#         app_url = APP_URL[str(value)]
#     except Exception as e:
#         print(e)
#         return app_url
#     return app_url