from django.shortcuts import render
from .models import Work
from .models import Cardboard_Box
from .models import Paper_Box


# Create your views here.
def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def first_page(request):
    return render(request, './index.html')


def req_data(request):
    a = int(request.GET['width'])
    b = int(request.GET['length'])
    c = int(request.GET['hight'])
    sum = int(request.GET['sum'])
    tray_hight = 30
    thickness_cb = 2
    cardboard = Cardboard_Box(a, b, c, thickness_cb)
    result_cardboard = cardboard.cardboard_box()
    paper = Paper_Box(a, b, c, thickness_cb)
    result_paper = paper.cub_box_paper()
    data = f'Размер коробки {a}x{b}x{c}мм. Высота крышки {tray_hight}. Картон {thickness_cb}мм. Тираж {sum}шт.'
    object_list = Work.objects.all()
    '''for obj in object_list:
        if obj.Name == 'крышка' and obj.dm2 <= result_cardboard[1]:
            lid = ((obj.dm2+obj.Content+obj.Scotch)+(obj.Close_fitting/sum))*obj.Lid
        elif obj.Name == 'тазик' and obj.dm2 <= result_cardboard[2]:
            tray = ((obj.dm2+obj.Content+obj.Scotch)+(obj.Close_fitting/sum))*obj.Tray'''
    return render(request, './result.html', {'data': data,
                                             'result_cardboard': result_cardboard,
                                             'result_paper': result_paper})
