from django.shortcuts import render
from .models import Order
from cardboard_box import cub_box
from paper_box import cub_box_paper


# Create your views here.
def first_page(request):
    object_list = Order.objects.all()
    return render(request, './index.html', {'object_list': object_list})


def req_data(request):

    a = request.GET['width']
    b = request.GET['length']
    c = request.GET['hight']
    result = cub_box(a, b, c, 2)
    result_2 = cub_box_paper(a, b, c, 2)

    return render(request, './result.html', {'result': result,
                                            'result_2': result_2})