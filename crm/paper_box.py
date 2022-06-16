import math
from calculation_algorithm import alg_calc as calc
import numpy as np


# бумага крышка
def lid_paper(x, y, lid_hight, thickness_cb, kink_paper):
    indent = 5
    c = math.sqrt((thickness_cb**2)+(thickness_cb**2))
    width = (lid_hight*2)+x+(thickness_cb*2)+1+(c*2)+(kink_paper*2)+indent
    length = (lid_hight*2)+y+(thickness_cb*2)+1+(c*2)+(kink_paper*2)+indent
    return [math.ceil(width), math.ceil(length)]


# бумага дно одним листом
def tray_paper_once(x, y, lid_hight, thickness_cb, kink_paper):
    indent = 5
    c = math.sqrt((thickness_cb**2)+(thickness_cb**2))
    width = (lid_hight*2)+x+(thickness_cb*2)+(c*2)+(kink_paper*2)+indent
    length = (lid_hight*2)+y+(thickness_cb*2)+(c*2)+(kink_paper*2)+indent
    return [math.ceil(width), math.ceil(length)]


# бумага дно бортом
def tray_paper_rim(x, y, tray_hight, thickness_cb, kink_paper):
    indent = 5
    c = math.sqrt((thickness_cb**2)+(thickness_cb**2))
    corner = thickness_cb**4
    width = tray_hight+kink_paper+c+thickness_cb+10+indent
    length = (x*2)+(y*2)+corner+20+indent
    return [[math.ceil(width), math.ceil(length)], [x-3, y-3]]


# бумага дно двумя бортами
def tray_paper_rim_tw(x, y, tray_hight, thickness_cb, kink_paper):
    indent = 5
    c = math.sqrt((thickness_cb**2)+(thickness_cb**2))
    corner = thickness_cb**4
    width = tray_hight+kink_paper+c+thickness_cb+10+indent
    length = x+y+(corner/2)+20+indent
    return [[math.ceil(width), math.ceil(length)], [x-3, y-3], [0, 0]]


# расход материала
def expence(lid, tray):
    lis_one = [lid, tray]
    lis_siz = [1000, 700]
    try:
        # результат дно и крышка вместе
        lid_ras = calc([lid], lis_siz)
        # результат дно и крышка раздельно
        a = np.size(tray)
        if a == 4:
            tray_bor = calc([tray[0]], lis_siz)
            tray_dno = calc([tray[1]], lis_siz)
            tray_ras = tray_bor[0] + tray_dno[0]
            return f'Расход - {lid_ras[0] + tray_ras}л;\nДонышко бортом;' \
                   f'\nКрышка - {lid[0]}x{lid[1]}мм;' \
                   f'\nБорт - {tray[0][0]}x{tray[0][1]}мм;\nДно - {tray[1][0]}x{tray[1][1]}мм.'
        elif a == 6:
            tray_bor = calc([tray[0]], lis_siz)*2
            tray_dno = calc([tray[1]], lis_siz)
            tray_ras = tray_bor[0] + tray_dno[0]
            return f'Расход - {lid_ras[0] + tray_ras}л;\nДонышко бортом;' \
                   f'\nКрышка - {lid[0]}x{lid[1]}мм;' \
                   f'\nБорт - {tray[0][0]}x{tray[0][1]}мм;\nДно - {tray[1][0]}x{tray[1][1]}мм.'
        else:
            tray_ras = calc([tray], lis_siz)[0]
            return f'Расход - {lid_ras[0] + tray_ras}л;\nДонышко одним листом;' \
                   f'\nКрышка - {lid[0]}x{lid[1]}мм;' \
                   f'\nДно - {tray[0]}x{tray[1]}мм.'
    except Exception:
        return Exception


def cub_box_paper(width, length, tray_hight, thickness_cb, lid_hight=30, kink_paper_lid=20, kink_paper_tray=20):
    lis_siz = [1000, 700]
    # бумага крышка
    lid_pap = lid_paper(width, length, lid_hight, thickness_cb, kink_paper_lid)
    if tray_hight <= 75:
        # бумага дно одним листом
        tray_pap = tray_paper_once(width, length, tray_hight, thickness_cb, kink_paper_tray)
    else:
        # бумага дно бортом
        tray_pap = tray_paper_rim(width, length, tray_hight, thickness_cb, kink_paper_tray)
        # бумага двумя бортами
        if tray_pap[0][1] > lis_siz[0]:
            tray_pap = tray_paper_rim_tw(width, length, tray_hight, thickness_cb, kink_paper_tray)

    try:
        result = expence(lid_pap, tray_pap)
        print('\nРасход бумаги')
        print(result)

    except ZeroDivisionError:
        print('Неполучилось расчитать.')


