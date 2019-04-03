from django.http import HttpRequest
from django.shortcuts import render, redirect

from .models import Item


def home_page(request: HttpRequest):
    # 处理POST请求
    # if request.method == 'POST':
    #     return render(request, 'home.html', {
    #         'new_item_text': request.POST['item_text']
    #     })

    # item = Item()
    # item.text = request.POST.get('item_text','')
    # item.save()
    # 重构上面3行代码，解决“每次GET请求都保存了一个空的待办事项”的问题

    # POST请求后应该重定向到列表页面
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    # 处理GET请求,在首页（列表页）显示待办事项列表
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
