from flask import Flask, render_template, request, jsonify  
import math 
import numpy as np  
import matplotlib.pyplot as plt  
import io  
import base64  

app = Flask(__name__)  

# 光速常量  
c = 299792458  # 光速 m/s  

def lorentz_transform(*args):  #*args表示可变参数，可以接受任意多个参数，args是一个元组
    """洛伦兹变换函数"""  
    #if len(args)==3:
    x=args[0]
    v=args[1]
    t=args[2]
    if v==0:
        return x,t   #如果速度为0，不变换
    else:
        gamma = 1 / math.sqrt(1 - (v**2))  # 计算洛伦兹因子        
        x_prime = gamma * (x - v * t* c)  
        t_prime = gamma * (t - (v * x) / c)  
        return x_prime, t_prime  
 
def create_world_line(velocities, time_range, ref_speed,DrawLines=[0,0]):  #velocities就是相对地面的速度
    """创建时空图像并返回图像字符串"""  
    #DrawLines是一个二维数组，第一个元素表示是画水平线的纵坐标，第二个元素表示画垂直线横坐标
    def mark_point(drawlines,ref_speed,velocities):
        #对某一特定速度进行转换
        #drawlines[1]是位移，drawlines[0]是时间
        #先计算相对静止系的物体的交点
        x_list=[drawlines[1]/v for v in velocities]
        x_list=np.array(x_list)
        y_list=[drawlines[0]*v for v in velocities]
        y_list=np.array(y_list)
        if(ref_speed!=0):
            x_list, y_list = lorentz_transform(x_list, ref_speed, y_list)  
        return x_list,y_list
            
            
        
    #函数来创建一个新的图形对象。这个函数定义在 Matplotlib 的 pyplot 模块中，用于生成和管理图形窗口
    plt.figure(figsize=(10, 6))  
    t = np.linspace(0, time_range, 100)  # 时间轴  
    for v in velocities:  
        x = v * c * t  # 计算在静止参考系下的位置 
    if ref_speed!=0:
        # 使用洛伦兹变换转换到新的参考系 
        x, t = lorentz_transform(x, ref_speed, t)  
    plt.plot(x, t, label=f'v = {v}c (ref v = {ref_speed}c)')  
    #画交线
    if DrawLines[1]:
        plt.axvline(DrawLines[1], color='red', lw=0.5,linestyle='--')  # 画垂直线
    if DrawLines[0]:
        plt.axhline(DrawLines[0], color='blue', lw=0.5,linestyle='--')
    
    # 计算交点
    x_prime,y_prime=mark_point(DrawLines,ref_speed,velocities)
    plt.plot(x_prime, y_prime, 'ro')  # 画交点
    for x, y in zip(x_prime, y_prime):
        plt.annotate(f'({x:.2f}, {y:.2f})', (x, y), textcoords="offset points", xytext=(5,5), ha='center')
    

    plt.title('World Lines in Spacetime Diagram')  
    plt.xlabel('Position (m) in new frame')  
    plt.ylabel('Time (s) in new frame')  
    plt.axhline(0, color='black', lw=0.5)  
    plt.axvline(0, color='black', lw=0.5)  
    plt.ylim(0, time_range)  
    plt.legend()  
    plt.grid()  
        
    # 保存图到内存并编码为 base64  
    buf = io.BytesIO()  
    plt.savefig(buf, format='png')  
    buf.seek(0)  
    img_str = base64.b64encode(buf.getvalue()).decode()  
    plt.close()  
    return img_str   

@app.route('/')  
def index():  
    return render_template('index.html')  

@app.route('/plot', methods=['POST'])  #这行代码定义了一个 URL 路由 /plot，并指定该路由只接受 POST 请求
def plot():  ##当访问 /plot 路由时会调用这个函数。
    data = request.get_json()  #请求中获取 JSON 数据，并将其解析为 Python 字典，存储在 data 变量中
    speeds_input = data.get('speeds')  
    ref_speed = data.get('ref_speed')  # 获取参考速度  
    time_range = data.get('time_range')  
    time_range=float(time_range)
    ref_speed=float(ref_speed)
    # 处理输入速度  将 speeds_input 字符串按逗号分割，并将每个分割后的字符串转换为浮点数，生成一个浮点数列表 velocities。
    velocities = [float(v) for v in speeds_input.split(',')]  
    
    # 生成时空图  
    img_str = create_world_line(velocities, time_range, ref_speed)  
    #将 img_str 包装在一个字典中，并使用 jsonify 函数将其转换为 JSON 格式的响应返回给客户端。
    return jsonify({'img_str': img_str})  

if __name__ == '__main__':  
    app.run(debug=True)