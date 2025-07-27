import pyvisa
import csv
import os
import time
from tkinter import Tk, Button, StringVar, Label
from tkinter.ttk import Combobox
from datetime import datetime



YPOSITION=0.0

click_count = 0
screenshot_count = 0
csv_path = None  # 初始化为None，在launch_gui时创建
selected_channel = None  

def connect_to_scope(target_resource=None):
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    if not resources:
        raise RuntimeError("未检测到任何 VISA 设备")
    if target_resource and target_resource in resources:
        scope = rm.open_resource(target_resource)
    else:
        scope = rm.open_resource(resources[0])
    scope.timeout = 10000
    scope.write_termination = '\n'
    scope.read_termination = '\n'
    return scope

def measure_once():
    global click_count
    channel = selected_channel.get()
    if not channel:
        print("请先选择通道")
        return
    try:
        scope = connect_to_scope('USB0::0x1AB1::0x044C::DHO9S262402321::INSTR')

        # 强制开启通道显示
        scope.write(f":{channel}:DISPlay ON")

        # 执行测量
        scope.write(f":MEASure:ITEM VAMP,{channel}")
        vamp_resp = scope.query(f":MEASure:ITEM? VAMP,{channel}").strip()
        vamp = float(vamp_resp)

        scope.write(f":MEASure:ITEM MARea,{channel}")
        area_resp = scope.query(f":MEASure:ITEM? MARea,{channel}").strip()
        area = float(area_resp)

        scope.close()
        click_count += 1
        print(f"[第{click_count}次点击] 通道 {channel} 幅度 VAMP = {vamp}, 面积 MARea = {area}")
        write_to_csv(click_count, vamp, area, channel)

    except Exception as e:
        print(f"测量出错：{e}")

def write_to_csv(count, vamp, area, channel):
    global csv_path
    header = ['点击次数', '通道', '幅度(VAMP)', '面积(MARea)', YPOSITION]
    row = [count, channel, vamp, area]
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if count == 1:  # 第一次写入时添加表头
            writer.writerow(header)
        writer.writerow(row)

def capture_screenshot():
    global screenshot_count
    try:
        scope = connect_to_scope('USB0::0x1AB1::0x044C::DHO9S262402321::INSTR')
        scope.write(":DISPlay:DATA? ON,PNG")  # 获取PNG图像数据
        raw_data = scope.read_raw()
        scope.close()

        screenshot_count += 1
        filename = f"screenshot_{screenshot_count}.png"
        with open(filename, "wb") as f:
            f.write(raw_data)

        print(f"已保存屏幕截图为：{filename}")

    except Exception as e:
        print(f"截图出错：{e}")

def launch_gui():
    global selected_channel, csv_path
    
    # 创建带有时间戳的CSV文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = f"measurements_{timestamp}.csv"

    window = Tk()
    window.title("示波器自动测量与截图")
    window.geometry("300x200")

    # 在创建 Tk 窗口之后初始化 StringVar
    selected_channel = StringVar(window)
    selected_channel.set("CHANnel1")  # 默认通道

    Label(window, text="选择通道：").pack(pady=(10, 0))
    channel_box = Combobox(window, textvariable=selected_channel, state="readonly")
    channel_box['values'] = ("CHANnel1", "CHANnel2", "CHANnel3", "CHANnel4")
    channel_box.current(0)
    channel_box.pack(pady=(0, 10))

    Button(window, text="执行测量", command=measure_once, height=2, width=20).pack(pady=5)
    Button(window, text="波形截图", command=capture_screenshot, height=2, width=20).pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    launch_gui()
