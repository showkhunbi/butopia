from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class ApiResponse(View):
    def post(self, *args, **kwargs):
        print(self.request.POST)
        return None
