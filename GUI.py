import PySimpleGUI as sg

from ctypes import *
from Core import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure


sizeX, sizeY = 0, 0
xGPU = []
yGPU = []
xMem = []
yMem = []


# главное окно
def main_window():
    sg.theme('LightBlue1')
    global sizeX, sizeY
    sizeX, sizeY = getSizeWindow(90)
    menu_def = [
        ['&Обновление данных', ['&Система', '&Информация о процессоре', '&Информация об ОЗУ', '&Информация о батареи',
                                '&Информация о ПЗУ', '&Информация о видеоадаптере', '&Обновить всё']]
    ]
    layout_sys_common = [[sg.Output(size=(round(sizeX * 0.04), 9), key='-sys_out_common-')]]
    layout_proc_info = [
        [sg.Text("", text_color='Black', background_color='LightBlue1', key='-procent_proc-'),
         sg.ProgressBar(100, orientation='h', size=(round(sizeX * 0.023), 20), bar_color=('Blue', 'LightBlue1'),
                       relief=sg.RELIEF_RAISED, key='-load_proc-')],
        [sg.Output(size=(round(sizeX * 0.04), 15), key='-proces_info-')]
    ]
    layout_memory_info = [
        [sg.Text("", text_color='Black', background_color='LightBlue1', key='-procent_mem-'),
         sg.ProgressBar(100, orientation='h', size=(round(sizeX * 0.013), 20), bar_color=('Blue', 'LightBlue1'),
                        relief=sg.RELIEF_RAISED, key='-load_mem-'),
         sg.Text("", text_color='Black', background_color='LightBlue1', key='-memory-')],
        [sg.Output(size=(round(sizeX * 0.04), 13), key='-memory_info-')]
    ]
    layout_battery_info = [[sg.Output(size=(round(sizeX * 0.04), 9), key='-battery_info-')]]
    layout_disk_info = [[sg.Output(size=(round(sizeX * 0.04), 16), key='-disk_info-')]]
    layout_net_info = [[sg.Output(size=(round(sizeX * 0.04), 15), key='-net_info-')]]
    layout_canvas_gpu = [[sg.Canvas(size=(round(sizeX * 0.04), 15), key='-CANVAS_GPU-')]]
    layout_canvas_memory = [[sg.Canvas(size=(round(sizeX * 0.04), 15), key='-CANVAS_MEM-')]]
    layout_gpu_info = [[sg.Output(size=(round(sizeX * 0.04), 9), key='-gpu_info-')]]
    layout = [
        [sg.Menu(menu_def)],
        [sg.Frame(layout=layout_sys_common, title='Общая информация о системе',
                  relief=sg.RELIEF_RAISED, tooltip='Система', title_color='Black', background_color='White'),
         sg.Frame(layout=layout_battery_info, title='Информация о батареи',
                  relief=sg.RELIEF_RAISED, tooltip='Питание', title_color='Black', background_color='White'),
         sg.Frame(layout=layout_gpu_info, title='Информация о GPU',
                  relief=sg.RELIEF_RAISED, tooltip='Видеокарта', title_color='Black', background_color='White')
         ],
        [sg.Frame(layout=layout_proc_info, title='Информация о процессоре',
                  relief=sg.RELIEF_RAISED, tooltip='Процессор', title_color='Black', background_color='White'),
         sg.Frame(layout=layout_disk_info, title='Информация о дисках хранения данных',
                  relief=sg.RELIEF_RAISED, tooltip='ПЗУ', title_color='Black', background_color='White'),
         sg.Frame(layout=layout_canvas_gpu, title='График загруженности процессора',
                  relief=sg.RELIEF_RAISED, tooltip='Процессор', title_color='Black', background_color='White')
         ],
        [sg.Frame(layout=layout_memory_info, title='Информация об оперативной памяти',
                  relief=sg.RELIEF_RAISED, tooltip='ОЗУ', title_color='Black', background_color='White'),
         sg.Frame(layout=layout_net_info, title='Информация о сети',
                  relief=sg.RELIEF_RAISED, tooltip='Сеть', title_color='Black', background_color='White'),
         sg.Frame(layout=layout_canvas_memory, title='График загруженности ОЗУ',
                  relief=sg.RELIEF_RAISED, tooltip='ОЗУ', title_color='Black', background_color='White')
         ]
    ]

    window = sg.Window('О компьютере', layout, size=(sizeX, sizeY), resizable=True, finalize=True,
                       grab_anywhere=True, element_justification='center')
    updateAll(window)
    axGPU, fig_aggGPU = createCanvasGPU(window)
    axMem, fig_aggMem = createCanvasMem(window)

    while True:
        event, values = window.read(timeout=700)
        window['-procent_mem-'].update(str(get_memory_percent()) + '%')
        window['-load_mem-'].update_bar(get_memory_percent())
        window['-memory-'].update(get_memory())
        processor = processor_info_percen()
        window['-procent_proc-'].update(str(processor) + '%')
        window['-load_proc-'].update_bar(processor)
        graphGPU(processor, axGPU, fig_aggGPU)
        graphMem(get_memory_used(), axMem, fig_aggMem)
        if event == 'Система':
            window['-sys_out_common-'].update(system_info())
        if event == 'Информация о процессоре':
            window['-proces_info-'].update(processor_info())
        if event == 'Информация об ОЗУ':
            window['-memory_info-'].update(memory_info())
        if event == 'Информация о ПЗУ':
            window['-disk_info-'].update(disk_info())
        if event == 'Информация о батареи':
            window['-battery_info-'].update(battery())
        if event == 'Информация о видеоадаптере':
            window['-gpu_info-'].update(gpu_temperature())
        if event == 'Обновить всё':
            updateAll(window)

        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    window.close()
    return


def getSizeWindow(percent: int):
    sizeX = windll.user32.GetSystemMetrics(0)
    sizeY = windll.user32.GetSystemMetrics(1)
    sizeX *= percent / 100
    sizeY *= percent / 120 #124
    return round(sizeX), round(sizeY)


def updateAll(window: sg.Window):
    window['-sys_out_common-'].update(system_info())
    processor = processor_info_percen()
    window['-procent_proc-'].update(str(processor) + '%')
    window['-load_proc-'].update_bar(processor)
    window['-proces_info-'].update(processor_info())
    window['-memory_info-'].update(memory_info())
    window['-procent_mem-'].update(str(get_memory_percent()) + '%')
    window['-load_mem-'].update_bar(get_memory_percent())
    window['-memory-'].update(get_memory())
    window['-disk_info-'].update(disk_info())
    window['-battery_info-'].update(battery())
    window['-net_info-'].update(net_info())
    window['-gpu_info-'].update(gpu_temperature())


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def graphGPU(temp, ax, fig_agg):
    global xGPU, yGPU
    yGPU.append(temp)
    xGPU.append(time())
    if len(xGPU) > 40:
        xGPU = xGPU[1:]
        yGPU = yGPU[1:]
        ax.cla()
    ax.plot(xGPU, yGPU, color='purple')
    fig_agg.draw()


def createCanvasGPU(window: sg.Window):
    canvas_elem = window['-CANVAS_GPU-']
    canvasProces = canvas_elem.TKCanvas

    # draw the initial plot in the window
    fig = Figure(figsize=(sizeX * 0.003, sizeY * 0.0032))
    ax = fig.add_subplot()
    ax.grid(True)
    fig_agg = draw_figure(canvasProces, fig)
    return ax, fig_agg


def createCanvasMem(window: sg.Window):
    canvas_elem = window['-CANVAS_MEM-']
    canvasMem = canvas_elem.TKCanvas
    # draw the initial plot in the window
    fig = Figure(figsize=(sizeX * 0.003, sizeY * 0.003))
    ax = fig.add_subplot()
    ax.grid(True)
    fig_agg = draw_figure(canvasMem, fig)
    return ax, fig_agg


def graphMem(temp, ax, fig_agg):
    global xMem
    global yMem
    yMem.append(temp)
    xMem.append(time())
    if len(xMem) > 40:
        xMem = xMem[1:]
        yMem = yMem[1:]
        ax.cla()
    ax.plot(xMem, yMem, color='purple')
    fig_agg.draw()