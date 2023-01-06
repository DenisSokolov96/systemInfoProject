import PySimpleGUI as sg
from ctypes import *

from Core import *


# главное окно
def main_window():
    sg.theme('LightBlue1')
    sizeX, sizeY = getSizeWindow(80)

    menu_def = [
        ['&Обновление таблиц', ['&Система', '&Информация о процессоре', '&Информация об ОЗУ', '&Информация о батареи',
                                '&Информация о ПЗУ']]
    ]
    layout_sys_common = [[sg.Output(size=(round(sizeX * 0.04), 9), key='-sys_out_common-')]]
    layout_proc_info = [[sg.Output(size=(round(sizeX * 0.04), 15), key='-proces_info-')]]
    layout_memory_info = [
        [sg.Text("", text_color='Black', background_color='LightBlue1', key='-procent_mem-'),
         sg.ProgressBar(100, orientation='h', size=(round(sizeX * 0.019), 20), bar_color=('Blue', 'LightBlue1'),
                        relief=sg.RELIEF_RAISED, key='-load_mem-')],
        [sg.Output(size=(round(sizeX * 0.04), 13), key='-memory_info-')]
    ]
    layout_battery_info = [[sg.Output(size=(round(sizeX * 0.04), 9), key='-battery_info-')]]
    layout_disk_info = [[sg.Output(size=(round(sizeX * 0.04), 15), key='-disk_info-')]]
    layout_net_info = [[sg.Output(size=(round(sizeX * 0.04), 15), key='-net_info-')]]
    layout = [
        [sg.Menu(menu_def)],
        [sg.Frame(layout=layout_sys_common, title='Общая информация о системе',
                  relief=sg.RELIEF_RAISED, tooltip='Система', title_color='Black', background_color='White'),
         sg.Frame(layout=layout_battery_info,
                  title='Информация о батареи',
                  relief=sg.RELIEF_RAISED, tooltip='Заряд', title_color='Black', background_color='White')
         ],
        [sg.Frame(layout=layout_proc_info,
                  title='Информация о процессоре',
                  relief=sg.RELIEF_RAISED, tooltip='Процессор', title_color='Black', background_color='White'),
         sg.Frame(layout=layout_disk_info,
                  title='Информация о дисках хранения данных',
                  relief=sg.RELIEF_RAISED, tooltip='ПЗУ', title_color='Black', background_color='White')
         ],
        [sg.Frame(layout=layout_memory_info,
                  title='Информация об оперативной памяти',
                  relief=sg.RELIEF_RAISED, tooltip='ОЗУ', title_color='Black', background_color='White'),
         sg.Frame(layout=layout_net_info,
                  title='Информация о сети',
                  relief=sg.RELIEF_RAISED, tooltip='Сеть', title_color='Black', background_color='White')
         ]
    ]

    window = sg.Window('О компьютере', layout, size=(sizeX, sizeY), resizable=True, finalize=True)

    window['-sys_out_common-'].update(system_info())
    window['-proces_info-'].update(processor_info())
    window['-memory_info-'].update(memory_info())
    window['-procent_mem-'].update(str(get_memory()) + '%')
    window['-load_mem-'].update_bar(get_memory())
    window['-disk_info-'].update(disk_info())
    window['-battery_info-'].update(battery())
    window['-net_info-'].update(net_info())

    while True:
        event, values = window.read()
        if event == 'Система':
            window['-sys_out_common-'].update(system_info())
        if event == 'Информация о процессоре':
            window['-proces_info-'].update(processor_info())
        if event == 'Информация об ОЗУ':
            window['-memory_info-'].update(memory_info())
            window['-procent_mem-'].update(str(get_memory()) + '%')
            window['-load_mem-'].update_bar(get_memory())
        if event == 'Информация о ПЗУ':
            window['-disk_info-'].update(disk_info())
        if event == 'Информация о батареи':
            window['-battery_info-'].update(battery())

        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    window.close()
    return


def getSizeWindow(percent: int):
    sizeX = windll.user32.GetSystemMetrics(0)
    sizeY = windll.user32.GetSystemMetrics(1)
    sizeX *= percent / 100
    sizeY *= percent / 115
    return round(sizeX), round(sizeY)
