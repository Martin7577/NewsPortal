# from django.http import HttpResponse
# from django.views import View
# from .task import send_mail
#
# class IndexView(View):
#     def get(self, request):
#         send_mail.delay()
#         return HttpResponse('Hello!')