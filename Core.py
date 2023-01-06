from psutil import *
from platform import *
import matplotlib.pyplot as plt
from time import sleep, strftime, time


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def secs_2_hours(secs):
    if secs == -2:
        return "не огранично"
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)


def battery():
    res = sensors_battery()
    strWrite = "\n"
    strWrite += "*" * 25 + "Информация о батареи" + "*" * 25 + "\n"
    try:
        strWrite += "* Уровень заряда: %s%%" % res.percent + "\n"
        strWrite += "* Время до разряда батареи: %s" % secs_2_hours(res.secsleft) + "\n"
        strWrite += "* Питание подключено" if res.power_plugged else "* Питание отключено"
    except Exception:
        strWrite += "Питание от сети" + "\n"
    strWrite += "\n"
    return strWrite


def system_info():
    strWrite = "\n"
    strWrite += "*" * 25 + "Системная информация" + "*" * 25 + "\n"
    data = uname()
    strWrite += f"* Система: {data.system}\n"
    strWrite += f"* Имя узла: {data.node}\n"
    strWrite += f"* Выпуск: {data.release}\n"
    strWrite += f"* Версия: {data.version}\n"
    strWrite += f"* Машина: {data.machine}\n"
    strWrite += f"* Процессор: {data.processor}\n"
    return strWrite


def processor_info():
    strWrite = "\n"
    strWrite += "*" * 23 + "Информация о процессоре" + "*" * 23 + "\n"
    strWrite += f"* Физические ядра:  {cpu_count(logical=False)}" + "\n"
    strWrite += f"* Всего ядер:  {cpu_count(logical=True)}" + "\n"
    cpufreq = cpu_freq()
    strWrite += f"* Максимальное частота: {cpufreq.max:.2f}МГц" + "\n"
    strWrite += f"* Минимальная частота: {cpufreq.min:.2f}МГц" + "\n"
    strWrite += f"* Текущая частота: {cpufreq.current:.2f}МГц" + "\n"
    strWrite += "* Загруженность процессора на ядро:" + "\n"
    for i, percentage in enumerate(cpu_percent(percpu=True, interval=1)):
        strWrite += " " * 5 + f"Ядро {i+1}: {percentage}%" + "\n"
    strWrite += f"* Общая загруженность процессора: {cpu_percent()}%" + "\n"
    return strWrite


def memory_info():
    strWrite = "\n"
    strWrite += "*" * 20 + "Информация об оперативной памяти" + "*" * 20 + "\n"
    svmen = virtual_memory()
    strWrite += f"* Объем: {get_size(svmen.total)}" + "\n"
    strWrite += f"* Доступно: {get_size(svmen.available)}" + "\n"
    strWrite += f"* Используется: {get_size(svmen.used)}" + "\n"
    strWrite += f"* Процент: {svmen.percent}%" + "\n"
    strWrite += "\n"
    strWrite += "*" * 20 + "Информация о памяти подкачки" + "*" * 20 + "\n"
    swap = swap_memory()
    strWrite += f"* Объем: {get_size(swap.total)}" + "\n"
    strWrite += f"* Свободно: {get_size(swap.free)}" + "\n"
    strWrite += f"* Используется: {get_size(swap.used)}" + "\n"
    strWrite += f"* Процент: {swap.percent}%" + "\n"
    return strWrite


def get_memory():
    return virtual_memory().percent


def disk_info():
    strWrite = "\n"
    strWrite = "*" * 14 + "Информация о дисках хранения данных" + "*" * 14 + "\n"
    partitions = disk_partitions()
    for partition in partitions:
        strWrite += f"*** Диск: {partition.device} ***" + "\n"
        strWrite += f"* - Тип файловой системы: {partition.fstype}" + "\n"
        try:
            partition_usage = disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        strWrite += f"* - Общий объём: {get_size(partition_usage.total)}" + "\n"
        strWrite += f"* - Используется: {get_size(partition_usage.used)}" + "\n"
        strWrite += f"* - Свободно: {get_size(partition_usage.free)}" + "\n"
        strWrite += f"* - Процент: {partition_usage.percent}%" + "\n"
    return strWrite


def net_info():
    strWrite = "\n"
    strWrite += "*" * 25 + "Информация о сети" + "*" * 25 + "\n"
    if_addrs = net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                strWrite += "\n"
                strWrite += f"*** Интерфейс: {interface_name} ***" + "\n"
                strWrite += f"* - IP: {address.address}" + "\n"
                strWrite += f"* - Сетевая маска: {address.netmask}" + "\n"
                strWrite += f"* - Широковещательный IP-адрес: {address.broadcast}" + "\n"
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                strWrite += "\n"
                strWrite += f"*** Интерфейс: {interface_name} ***" + "\n"
                strWrite += f"* - MAC-адрес: {address.address}" + "\n"
                strWrite += f"* - Сетевая маска: {address.netmask}" + "\n"
                strWrite += f"* - Широковещательный MAC: {address.broadcast}" + "\n"
    net_io = net_io_counters()
    strWrite += f"* Общее кол-во отправленных данных: {get_size(net_io.bytes_sent)}" + "\n"
    strWrite += f"* Общее кол-во пполученных данных: {get_size(net_io.bytes_recv)}" + "\n"
    return strWrite


def sensor_fan_info():
    sens_fans = None
    try:
        sens_fans = sensors_fans()
    except Exception as ex:
        print()
        print(f"* Вращение вентиляторов - недоступно")
        print(f"* {ex}")
        return
    print()
    print(f"* Вращение вентиляторов: {sens_fans}")


def sensor_temper_info():
    sens_temper = None
    try:
        sens_temper = sensors_temperatures()
    except Exception as ex:
        print()
        print(f"* Температура - недоступно")
        print(f"* {ex}")
        return
    print()
    print(f"* Температура: {sens_temper}")


"""
Для графика
"""
# plt.ion()
# x = []
# y = []
# def graph(temp):
#     y.append(temp)
#     x.append(time())
#     plt.clf()
#     plt.scatter(x, y)
#     plt.plot(x, y)
#     plt.draw()

