from django.http import HttpRequest
from django.shortcuts import render, redirect

from .models import Item, List


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

    # 处理GET请求,在首页（列表页）显示待办事项列表
    return render(request, 'home.html')


def view_list(request, list_id):
    a_list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': a_list})


def new_list(request):
    a_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=a_list)
    return redirect(f'/lists/{a_list.id}/')


def add_item(request, list_id, ):
    a_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=a_list)

    return redirect(f'/lists/{a_list.id}/')
