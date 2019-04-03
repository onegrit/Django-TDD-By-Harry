from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_page(request: HttpRequest):
    # 处理POST请求
    # if request.method == 'POST':
    #     return render(request, 'home.html', {
    #         'new_item_text': request.POST['item_text']
    #     })
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text','')
    })

    # return render(request, 'home.html')
