from calculation_algorithm import alg_calc as calc


# картонная крышка
def lid_cb(x, y, lid_hight, thickness_cb):
    indent = 5
    width = (lid_hight*2)+x+(thickness_cb*2)+2+indent
    length = (lid_hight*2)+y+(thickness_cb*2)+2+indent
    return [width, length]


# картонное дно
def tray_cb(x, y, tray_hight):
    indent = 10
    width = (tray_hight*2)+x+indent
    length = (tray_hight*2)+y+indent
    return [width, length]


# расчет отдельно крышка и дно
def sep_lid_tray(lid, tray, lis_siz):

    # проверка крышки
    ras_lid = calc([lid], lis_siz)

    # проверка дна
    ras_tray = calc([tray], lis_siz)

    result = ras_lid[0] + ras_tray[0]
    return result


# расход материала
def expence(lid, tray):
    lis_one = [lid, tray]
    lis_siz = [1000, 700]
    try:
        # четыре варианта располодения крышки и дно вместе
        lis_tw = [[tray[0], lid[1] + tray[1]], [tray[0] + lid[0], tray[1]],
                  [tray[0], lid[0] + tray[1]], [lid[1] + tray[0], lid[0]]]

        # результат дно и крышка вместе
        result_tw = calc(lis_tw, lis_siz)
        # результат дно и крышка раздельно
        result_one = sep_lid_tray(lid, tray, lis_siz)

        if result_tw[0] <= result_one:
            return f'Расход - {result_tw[0]}л; \nКрышка и дно вместе;' \
                   f'\nКрышка - {result_tw[1][0]}x{result_tw[1][1]}мм.'
        else:
            return f'Расход - {result_one}л; \nКрышка и дно раздельно;' \
                   f'\nКрышка - {lis_one[0][0]}x{lis_one[0][1]}мм;' \
                   f''f'\nДно - {lis_one[1][0]}x{lis_one[1][1]}мм.'

    except ZeroDivisionError:
        result = sep_lid_tray(lid, tray, lis_siz)
        return f'Расход - {result}л; \nКрышка и дно раздельно;'\
               f'\nКрышка - {lis_one[0][0]}x{lis_one[0][1]}мм;' \
               f''f'\nДно - {lis_one[1][0]}x{lis_one[1][1]}мм.'


def cub_box(width, length, tray_hight, thickness_cb, lid_hight=30):
    # развернутая крышка
    lid_card = lid_cb(width, length, lid_hight, thickness_cb)
    # развернутое дно
    tray_card = tray_cb(width, length, tray_hight)

    try:
        result = expence(lid_card, tray_card)
        print(f'Размер коробки {width}x{length}x{tray_hight}мм;'
              f'\nВысота крышки {lid_hight}мм;'
              f'\nКартон {thickness_cb}мм;')
        print('\nРасход картона')
        print(result)
    except ZeroDivisionError:
        print('Неполучилось разместить на листе.')

