import clr, os, winreg
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime

#注：手动停止之后一定要进行一次ZEMAX重启，否则无法打开追迹工具

# 变量设置区域
##################################################################################
##################################################################################
# 7.9更新，修改为同时修改两个坐标，然后进行一次追迹，最后获取一次数据
# 2号物体步长
STEP_SIZE_OBJECT2 = 0.01
# 3号物体步长
STEP_SIZE_OBJECT3 = 0.01

#总次数，计算方法为区间长度除以步长,可选择加一，因为比如0-100，步长为1，要想形成左闭右闭区间，要加一
TOTAL_RUNS = 100


##################################################################################
##################################################################################
##################################################################################



def initialize_connection():
    """初始化Zemax连接并返回必要的对象"""
    # === 初始化连接 ===
    aKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Zemax")
    zemaxData = winreg.QueryValueEx(aKey, 'ZemaxRoot')
    winreg.CloseKey(aKey)

    clr.AddReference(os.path.join(zemaxData[0], 'ZOS-API\Libraries\ZOSAPI_NetHelper.dll'))
    import ZOSAPI_NetHelper

    ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize()
    zemaxDir = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory()

    clr.AddReference(os.path.join(zemaxDir, 'ZOSAPI.dll'))
    clr.AddReference(os.path.join(zemaxDir, 'ZOSAPI_Interfaces.dll'))
    import ZOSAPI
    

    TheConnection = ZOSAPI.ZOSAPI_Connection()
    TheApplication = TheConnection.ConnectAsExtension(0)

    if not TheApplication.IsValidLicenseForAPI:
        raise Exception("ZOSAPI 授权无效")

    TheSystem = TheApplication.PrimarySystem
    if TheSystem is None:
        raise Exception("未检测到当前系统")
        
    return TheSystem, ZOSAPI



#已弃用
##############################################
# def set_wolter_z_position(TheSystem, ZOSAPI):
#     nce = TheSystem.NCE
#     nce.GetObjectAt(8).YPosition += STEP_SIZE
##############################################


# 以下是修改坐标的函数

def set_which_XPosition(TheSystem,xnum,step):
    nce = TheSystem.NCE
    nce.GetObjectAt(xnum).XPosition += step



def set_which_YPosition(TheSystem,ynum,step):
    nce = TheSystem.NCE
    nce.GetObjectAt(ynum).YPosition += step


def set_which_ZPosition(TheSystem,znum,step):
    nce = TheSystem.NCE
    nce.GetObjectAt(znum).ZPosition += step

##############################################################

# 以下是获取坐标的函数
def get_which_XPosition(TheSystem,xnum):
    nce = TheSystem.NCE
    return nce.GetObjectAt(xnum).XPosition


def get_which_YPosition(TheSystem,ynum):
    nce = TheSystem.NCE
    return nce.GetObjectAt(ynum).YPosition



def get_which_ZPosition(TheSystem,znum):
    nce = TheSystem.NCE
    return nce.GetObjectAt(znum).ZPosition


##############################################################
##############################################################
##############################################################
def run_nsc_ray_trace(TheSystem):
    # === 1. 执行 NSC 光线追迹（这里不执行追迹，只是打开工具） ===
    try:
        NSCRayTrace = TheSystem.Tools.OpenNSCRayTrace()

        # 配置参数
        NSCRayTrace.ClearDetectors(0)  # 清除探测器数据


        NSCRayTrace.SplitNSCRays = False
        NSCRayTrace.ScatterNSCRays = False
        NSCRayTrace.UsePolarization = False
        NSCRayTrace.IgnoreErrors = True
        NSCRayTrace.SaveRays = False

        # 运行光线追迹并等待完成
        NSCRayTrace.RunAndWaitForCompletion()

        # 关闭工具
        NSCRayTrace.Close()
    except:
        raise Exception("无法打开 NSC 光线追迹工具")




########
# 已修改，变为两个参数
#  def get_detector_total_power(TheSystem, ZOSAPI, number, csv_writer, position1,position2):
# 数值为外部传参，里面只需要修改写入逻辑即可,为下面两句
#  csv_writer.writerow([position1, position2, power_value])
#  csv_writer.writerow([position1, position2 ,0.0])  # 如果没有找到，记录0

def get_detector_total_power(TheSystem, ZOSAPI, number, csv_writer, position1,position2):
    """获取探测器的Total Power数据"""
    # === 2. 获取 Detector Viewer 中的 Total Power ===
    TheAnalysis = TheSystem.Analyses.New_Analysis(ZOSAPI.Analysis.AnalysisIDM.DetectorViewer)

    # 创建数据保存目录
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)

    # 保存结果到data文件夹
    output_path = os.path.join(data_dir, f"detector{number}.txt")
    results = TheAnalysis.GetResults()
    results.GetTextFile(output_path)

    with open(output_path, 'r', encoding='utf-16') as f:
        text_data = f.read()

    print("=== Detector Viewer Text Output ===")
    found = False
    for line in text_data.splitlines():
        if "Total Power" in line:
            print(line)
            # 从行中提取Total Power值，移除单位后再转换为浮点数
            power_str = line.split(':')[1].strip()
            power_value = float(power_str.split()[0])  # 只取数值部分，忽略'Watts'单位
            # 将位置和功率写入CSV
            csv_writer.writerow([position1, position2, power_value])
            found = True

    if not found:
        print("未找到 'Total Power' 字段")
        csv_writer.writerow([position1, position2 ,0.0])  # 如果没有找到，记录0

    TheAnalysis.Close()

def main():
    """主函数"""
    
    # 获取当前时间并格式化为文件名
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = os.path.join(os.path.dirname(__file__), f"{current_time}_data.csv")
    
    for i in range(TOTAL_RUNS):
        # 每次循环都重新打开CSV文件进行追加
        with open(csv_filename, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            
            # 如果是第一次循环，写入表头

            #表头修改
            if i == 0:
                csv_writer.writerow(['Obj2Position','Obj3Position', 'Total Power'])
            
        
            ##7.9更新主函数，流程为同时修改两次坐标，然后进行一次追迹，最后获取一次数据
            TheSystem, ZOSAPI = initialize_connection()
            xposition2=get_which_XPosition(TheSystem,2)
            xposition3=get_which_XPosition(TheSystem,3)
            print(f"Round:{i+1}||Object2_X:{xposition2}||Object3_X:{xposition3}")
            run_nsc_ray_trace(TheSystem)
            get_detector_total_power(TheSystem, ZOSAPI, i, csv_writer,xposition2, xposition3)
            set_which_XPosition(TheSystem,2,STEP_SIZE_OBJECT2)
            set_which_XPosition(TheSystem,3,STEP_SIZE_OBJECT3)
            ##################################################################


# TODO
# 1. 画图部分模块封装
           
if __name__ == "__main__":
    main()
