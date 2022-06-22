from django.shortcuts import render
from .models import Work
from .models import Material
from .models import calc_count
from .models import Cardboard_Box
from .models import Paper_Box


# Create your views here.
def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def first_page(request):
    return render(request, './index.html')


def req_data(request):
    try:
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
        for obj in object_list:
            if obj.Name == 'крышка' and obj.dm2 <= result_paper[2]:
                lid = ((obj.dm2+obj.Content+obj.Scotch)+(obj.Close_fitting/sum))*obj.Lid
            elif obj.Name == 'тазик' and obj.dm2 <= result_paper[3]:
                tray = ((obj.dm2+obj.Content+obj.Scotch)+(obj.Close_fitting/sum))*obj.Tray

        cardboard_req = request.GET['cardboard']
        paper_req = request.GET['paper']
        currency_req = request.GET['currency']
        currency = {'euro': float(currency_req), 'rub': 1}

        data_calc = calc_count.objects.get(pk=1)
        paper_obj = Material.objects.get(mt_name= paper_req)
        paper_count = (paper_obj.prise * (currency.get(paper_obj.currency))*float(result_paper[0]))
        cardboard_obj = Material.objects.get(mt_name= cardboard_req)
        cardboard_count = (cardboard_obj.prise * (currency.get(cardboard_obj.currency))*float(result_cardboard[0]))

        calc_sum = ((paper_count+cardboard_count)*data_calc.reject+data_calc.cut+(lid+tray)+((lid+tray)*data_calc.not_production))\
                   *data_calc.margin

        return render(request, './result.html', {'data': data,
                                                 'result_cardboard_0': result_cardboard[0],
                                                 'result_cardboard_1': result_cardboard[1],
                                                 'result_paper_0': result_paper[0], 'result_paper_1': result_paper[1],
                                                 'work': toFixed(lid+tray, 2),
                                                 'cardboard': cardboard_req, 'paper': paper_req,
                                                 'sum': toFixed(calc_sum, 2)})
    except Exception:
        return render(request, './result_ex.html')

