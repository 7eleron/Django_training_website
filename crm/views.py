from django.shortcuts import render
from .models import Order
from .models import Cardboard_Box
from .models import Paper_Box
#from paper_box import cub_box_paper


# Create your views here.
def first_page(request):
    object_list = Order.objects.all()
    return render(request, './index.html', {'object_list': object_list})


def req_data(request):
    a = int(request.GET['width'])
    b = int(request.GET['length'])
    c = int(request.GET['hight'])
    tray_hight = 30
    thickness_cb = 2
    cardboard = Cardboard_Box(a, b, c, thickness_cb)
    result_cardboard = cardboard.cardboard_box()
    paper = Paper_Box(a, b, c, thickness_cb)
    result_paper = paper.cub_box_paper()
    data = f'Размер коробки {a}x{b}x{c}мм. Высота крышки {tray_hight}. Картон {thickness_cb}мм.'

    return render(request, './result.html', {'data': data,
                                             'result_cardboard': result_cardboard,
                                             'result_paper': result_paper})