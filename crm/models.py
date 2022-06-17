from django.db import models
import numpy as np
import math


# Create your models here.
class Order(models.Model):
    order_dt = models.DateTimeField(auto_now=True)
    order_name = models.CharField(max_length=200, verbose_name='Name')
    order_phone = models.CharField(max_length=200, verbose_name='Telephone')

    def __str__(self):
        return self.order_name

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


def calc(lis, lis_siz):
    kol_lis = 0
    var = None
    for x in lis:
        # проход по длинной стороне
        ras_0 = (lis_siz[0]//x[0])*(lis_siz[1]//x[1])
        ras_ost_0 = [[lis_siz[0] % x[0], lis_siz[1]], [lis_siz[1] % x[1], lis_siz[0]]]
        kol_ost_ras_0_1 = (ras_ost_0[0][0] // x[1]) * (ras_ost_0[0][1] // x[0])
        kol_ost_ras_0_2 = (ras_ost_0[0][0] // x[0]) * (ras_ost_0[0][1] // x[1])

        if kol_ost_ras_0_1 > kol_ost_ras_0_2:
            kol_dop_ras_0 = kol_ost_ras_0_1
        else:
            kol_dop_ras_0 = kol_ost_ras_0_2

        # проход по короткой стороне
        ras_1 = (lis_siz[0]//x[1])*(lis_siz[1]//x[0])
        ras_ost_1 = [[lis_siz[0] % x[1], lis_siz[1]], [lis_siz[1] % x[0], lis_siz[0]]]
        kol_ost_ras_1_1 = (ras_ost_1[0][0] // x[1]) * (ras_ost_1[0][1] // x[0])
        kol_ost_ras_1_2 = (ras_ost_1[0][0] // x[0]) * (ras_ost_1[0][1] // x[1])

        if kol_ost_ras_1_1 > kol_ost_ras_1_2:
            kol_dop_ras_1 = kol_ost_ras_1_1
        else:
            kol_dop_ras_1 = kol_ost_ras_1_2

        # добавление количества с листа
        if ras_0 >= ras_1:
            if ras_0 >= kol_lis:
                kol_lis = ras_0 + kol_dop_ras_0
                var = x
        else:
            if ras_1 >= kol_lis:
                kol_lis = ras_1 + kol_dop_ras_1
                var = x

    result = 1 / kol_lis
    return [result, var]


class Cardboard_Box:
    def __init__(self, width, length, tray_hight, thickness_cb, lid_hight=30):
        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb
        self.lid_hight = lid_hight

    # картонная крышка
    def lid_cb(self, x, y, lid_hight, thickness_cb):
        indent = 5
        width = (lid_hight*2)+x+(thickness_cb*2)+2+indent
        length = (lid_hight*2)+y+(thickness_cb*2)+2+indent
        return [width, length]

    # картонное дно
    def tray_cb(self, x, y, tray_hight):
        indent = 10
        width = (tray_hight*2)+x+indent
        length = (tray_hight*2)+y+indent
        return [width, length]

    # расчет отдельно крышка и дно
    def sep_lid_tray(self, lid, tray, lis_siz):
        # проверка крышки
        ras_lid = calc([lid], lis_siz)

        # проверка дна
        ras_tray = calc([tray], lis_siz)

        result = ras_lid[0] + ras_tray[0]
        return result

    # расход материала
    def expence(self, lid, tray):
        lis_one = [lid, tray]
        lis_siz = [1000, 700]
        try:
            # четыре варианта располодения крышки и дно вместе
            lis_tw = [[tray[0], lid[1] + tray[1]], [tray[0] + lid[0], tray[1]],
                      [tray[0], lid[0] + tray[1]], [lid[1] + tray[0], lid[0]]]

            # результат дно и крышка вместе
            result_tw = calc(lis_tw, lis_siz)
            # результат дно и крышка раздельно
            result_one = self.sep_lid_tray(lid, tray, lis_siz)

            if result_tw[0] <= result_one:
                return f'- {result_tw[0]}л. Крышка и дно вместе. ' \
                       f'Крышка-дно - {result_tw[1][0]}x{result_tw[1][1]}мм.'
            else:
                return f'- {result_one}л. Крышка и дно раздельно. ' \
                       f'Крышка - {lis_one[0][0]}x{lis_one[0][1]}мм. ' \
                       f'Дно - {lis_one[1][0]}x{lis_one[1][1]}мм.'

        except ZeroDivisionError:
            result = self.sep_lid_tray(lid, tray, lis_siz)
            return f'- {result}л.Крышка и дно раздельно. '\
                   f'Крышка - {lis_one[0][0]}x{lis_one[0][1]}мм. ' \
                   f'Дно - {lis_one[1][0]}x{lis_one[1][1]}мм.'

    def cardboard_box(self):
        # развернутая крышка
        lid_card = self.lid_cb(self.width, self.length, self.lid_hight, self.thickness_cb)
        # развернутое дно
        tray_card = self.tray_cb(self.width, self.length, self.lid_hight,)

        try:
            result = self.expence(lid_card, tray_card)
            return f'Расход картона {result}'
        except ZeroDivisionError:
            return 'Неполучилось разместить на листе.'


class Paper_Box:
    def __init__(self, width, length, tray_hight, thickness_cb, lid_hight=30, kink_paper_lid=20, kink_paper_tray=20):

        self.width = width
        self.length = length
        self.tray_hight = tray_hight
        self.thickness_cb = thickness_cb
        self.lid_hight = lid_hight
        self.kink_paper_lid = kink_paper_lid
        self.kink_paper_tray = kink_paper_tray

    # бумага крышка
    def lid_paper(self, x, y, lid_hight, thickness_cb, kink_paper):
        indent = 5
        c = math.sqrt((thickness_cb ** 2) + (thickness_cb ** 2))
        width = (lid_hight * 2) + x + (thickness_cb * 2) + 1 + (c * 2) + (kink_paper * 2) + indent
        length = (lid_hight * 2) + y + (thickness_cb * 2) + 1 + (c * 2) + (kink_paper * 2) + indent
        return [math.ceil(width), math.ceil(length)]

    # бумага дно одним листом
    def tray_paper_once(self, x, y, lid_hight, thickness_cb, kink_paper):
        indent = 5
        c = math.sqrt((thickness_cb ** 2) + (thickness_cb ** 2))
        width = (lid_hight * 2) + x + (thickness_cb * 2) + (c * 2) + (kink_paper * 2) + indent
        length = (lid_hight * 2) + y + (thickness_cb * 2) + (c * 2) + (kink_paper * 2) + indent
        return [math.ceil(width), math.ceil(length)]

    # бумага дно бортом
    def tray_paper_rim(self, x, y, tray_hight, thickness_cb, kink_paper):
        indent = 5
        c = math.sqrt((thickness_cb ** 2) + (thickness_cb ** 2))
        corner = thickness_cb ** 4
        width = tray_hight + kink_paper + c + thickness_cb + 10 + indent
        length = (x * 2) + (y * 2) + corner + 20 + indent
        return [[math.ceil(width), math.ceil(length)], [x - 3, y - 3]]

    # бумага дно двумя бортами
    def tray_paper_rim_tw(self, x, y, tray_hight, thickness_cb, kink_paper):
        indent = 5
        c = math.sqrt((thickness_cb ** 2) + (thickness_cb ** 2))
        corner = thickness_cb ** 4
        width = tray_hight + kink_paper + c + thickness_cb + 10 + indent
        length = x + y + (corner / 2) + 20 + indent
        return [[math.ceil(width), math.ceil(length)], [x - 3, y - 3], [0, 0]]

    # расход материала
    def expence(self, lid, tray):
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
                return f'- {lid_ras[0] + tray_ras}л. Донышко бортом.' \
                       f' Крышка - {lid[0]}x{lid[1]}мм. ' \
                       f'Борт - {tray[0][0]}x{tray[0][1]}мм. Дно - {tray[1][0]}x{tray[1][1]}мм.'
            elif a == 6:
                tray_bor = calc([tray[0]], lis_siz) * 2
                tray_dno = calc([tray[1]], lis_siz)
                tray_ras = tray_bor[0] + tray_dno[0]
                return f'- {lid_ras[0] + tray_ras}л. Донышко бортом.' \
                       f'Крышка - {lid[0]}x{lid[1]}мм. ' \
                       f'Борт - {tray[0][0]}x{tray[0][1]}мм. Дно - {tray[1][0]}x{tray[1][1]}мм.'
            else:
                tray_ras = calc([tray], lis_siz)[0]
                return f'- {lid_ras[0] + tray_ras}л. Донышко одним листом. ' \
                       f'Крышка - {lid[0]}x{lid[1]}мм. ' \
                       f'Дно - {tray[0]}x{tray[1]}мм.'
        except Exception:
            return Exception

    def cub_box_paper(self):
        lis_siz = [1000, 700]
        # бумага крышка
        lid_pap = self.lid_paper(self.width, self.length, self.lid_hight, self.thickness_cb, self.kink_paper_lid)
        if self.tray_hight <= 75:
            # бумага дно одним листом
            tray_pap = self.tray_paper_once(self.width, self.length, self.tray_hight, self.thickness_cb, self.kink_paper_tray)
        else:
            # бумага дно бортом
            tray_pap = self.tray_paper_rim(self.width, self.length, self.tray_hight, self.thickness_cb, self.kink_paper_tray)
            # бумага двумя бортами
            if tray_pap[0][1] > lis_siz[0]:
                tray_pap = self.tray_paper_rim_tw(self.width, self.length, self.tray_hight, self.thickness_cb, self.kink_paper_tray)

        try:
            result = self.expence(lid_pap, tray_pap)
            return f'Расход бумаги {result}'

        except ZeroDivisionError:
            return 'Неполучилось расчитать.'
