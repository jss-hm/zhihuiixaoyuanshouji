from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from datetime import datetime


# 关键修正：获取app文件夹的上级目录（因为static和app同级）
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # app文件夹的绝对路径
PARENT_DIR = os.path.dirname(BASE_DIR)  # app文件夹的上级目录（static在这里）

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),  # 模板文件夹：app/templates
    static_folder=os.path.join(PARENT_DIR, 'static'),  # 静态文件夹：上级目录/static
    static_url_path='/static'  # 静态文件访问URL前缀保持为/static
)

app.secret_key = "campus_wise_system_2025"

# 模拟校园数据
data = {
    'announcements': [
        {'time': '2025-11-01', 'title': '期中考试通知', 'content': '11月15日进行期中考试，请携带学生证。'},
        {'time': '2025-10-28', 'title': '校园招聘会', 'content': '11月20日体育馆举办招聘会，欢迎毕业生参加。'},
    ],
    'courses': [
        {'name': 'Python编程', 'teacher': '李老师', 'time': '周一 08:30-10:00', 'location': '教学楼A302'},
        {'name': '数据结构', 'teacher': '王老师', 'time': '周二 10:20-11:50', 'location': '实验楼B201'},
    ],
    'scores': [
        {'course': 'Python编程', 'score': '92', 'credit': '3.0'},
        {'course': '数据结构', 'score': '88', 'credit': '3.5'},
    ],
    'user_info': {
        'name': '测试员',
        'student_id': '2024001',
        'major': '数媒',
        'grade': '2024级',
        'college': '计算机学院',
        'phone': '1678900',
        'service_reserve': '图书馆座位 9月15日',
        'settings': {
            'notify': True,
            'security': True,
            'update': False,
            'dark_mode': False
        }
    }
}

# 定义模块信息
modules = [
    {'name': '安全', 'icon': 'App安全.png', 'route': 'safety'},
    {'name': '宿舍', 'icon': 'App宿舍.png', 'route': 'dormitory'},
    {'name': '教育', 'icon': 'App教育.png', 'route': 'education'},
    {'name': '环境监测', 'icon': 'App环境监测.png', 'route': 'environment'},
    {'name': '食堂', 'icon': 'App食堂.png', 'route': 'canteen'}
]


# 首页路由
@app.route('/')
def index():
    return render_template(
        'index.html',
        modules=modules,
        announcements=data['announcements'],
        courses=data['courses'],
        scores=data['scores'],
        user=data['user_info']
    )


# -------------------------- 我的中心及编辑页面路由 --------------------------
@app.route('/mine')
def mine():
    user = data['user_info']
    settings = user['settings']
    return render_template('mine.html', user=user, settings=settings)


@app.route('/edit_info', methods=['GET', 'POST'])
def edit_info():
    user = data['user_info']
    if request.method == 'POST':
        user['name'] = request.form.get('name', user['name'])
        user['student_id'] = request.form.get('student_id', user['student_id'])
        user['college'] = request.form.get('college', user['college'])
        user['major'] = request.form.get('major', user['major'])
        user['phone'] = request.form.get('phone', user['phone'])
        return redirect(url_for('mine'))
    return render_template('edit_info.html', user=user)


@app.route('/edit_service', methods=['GET', 'POST'])
def edit_service():
    user = data['user_info']
    if request.method == 'POST':
        service_type = request.form.get('serviceType', '图书馆座位')
        service_date = request.form.get('serviceDate', '2025-09-15')
        date_obj = datetime.strptime(service_date, '%Y-%m-%d')
        formatted_date = f"{date_obj.month}月{date_obj.day}日"
        user['service_reserve'] = f"{service_type} {formatted_date}"
        return redirect(url_for('mine'))
    return render_template('edit_service.html', user=user)


@app.route('/edit_settings', methods=['GET', 'POST'])
def edit_settings():
    user = data['user_info']
    if request.method == 'POST':
        user['settings']['notify'] = request.form.get('notifySwitch') == 'on'
        user['settings']['security'] = request.form.get('securitySwitch') == 'on'
        user['settings']['update'] = request.form.get('updateSwitch') == 'on'
        user['settings']['dark_mode'] = request.form.get('darkModeSwitch') == 'on'
        return redirect(url_for('mine'))
    return render_template('edit_settings.html', settings=user['settings'])


# -------------------------- 新增：头像上传路由 --------------------------
@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    try:
        # ------------ 关键修改：直接写死 static 文件夹的绝对路径 ------------
        # 请手动修改为你的 static 文件夹真实路径！！！
        # 示例（Windows）：static_dir = r"D:\智慧校园\static"
        # 示例（Linux/macOS）：static_dir = "/home/xxx/智慧校园/static"
        static_dir = r"你的static文件夹绝对路径"  # 必须修改这里！
        # -------------------------------------------------------------------

        print("=" * 50)
        print("当前静态目录：", static_dir)

        # 1. 检查文件是否上传
        if 'avatar' not in request.files:
            print("错误：未收到头像文件")
            return {"status": "error", "msg": "未选择文件"}, 400

        file = request.files['avatar']
        if file.filename == '':
            print("错误：文件名为空")
            return {"status": "error", "msg": "未选择文件"}, 400

        # 2. 只允许图片（简化验证）
        if not file.type.startswith('image/'):
            print(f"错误：非图片文件，类型：{file.type}")
            return {"status": "error", "msg": "请上传图片"}, 400

        # 3. 强制创建 static 目录（不管是否存在）
        os.makedirs(static_dir, exist_ok=True)
        print("静态目录已确保存在")

        # 4. 保存文件（强制覆盖，用二进制模式）
        save_path = os.path.join(static_dir, 'avatar.png')
        with open(save_path, 'wb') as f:
            f.write(file.read())  # 直接读取文件内容写入，绕开 Flask 的 save 方法
        print(f"文件已保存到：{save_path}")
        print(f"文件大小：{os.path.getsize(save_path)} 字节")

        return {"status": "success", "msg": "上传成功"}, 200

    except Exception as e:
        # 打印最详细的错误信息
        import traceback
        print("=" * 50)
        print("上传失败详细日志：")
        traceback.print_exc()  # 打印完整错误堆栈
        return {"status": "error", "msg": str(e)}, 500


# -------------------------- 原有模块路由 --------------------------
@app.route('/safety')
def safety():
    return f"""
    <html>
        <head>
            <title>校园安全</title>
            <style>
                body {{ font-family: "Microsoft YaHei"; padding: 20px; }}
                .back {{ color: #86a8e7; text-decoration: none; }}
                .container {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <a href="/" class="back">← 返回首页</a>
            <div class="container">
                <h2>校园安全模块</h2>
                <p>这里是校园安全相关内容</p>
            </div>
        </body>
    </html>
    """


@app.route('/dormitory')
def dormitory():
    return f"""
    <html>
        <head>
            <title>宿舍管理</title>
            <style>
                body {{ font-family: "Microsoft YaHei"; padding: 20px; }}
                .back {{ color: #86a8e7; text-decoration: none; }}
                .container {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <a href="/" class="back">← 返回首页</a>
            <div class="container">
                <h2>宿舍管理模块</h2>
                <p>这里是宿舍管理相关内容</p>
            </div>
        </body>
    </html>
    """


@app.route('/education')
def education():
    return f"""
    <html>
        <head>
            <title>教育管理</title>
            <style>
                body {{ font-family: "Microsoft YaHei"; padding: 20px; }}
                .back {{ color: #86a8e7; text-decoration: none; }}
                .container {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <a href="/" class="back">← 返回首页</a>
            <div class="container">
                <h2>教育管理模块</h2>
                <p>这里是教育管理相关内容</p>
            </div>
        </body>
    </html>
    """


@app.route('/environment')
def environment():
    return f"""
    <html>
        <head>
            <title>环境监测</title>
            <style>
                body {{ font-family: "Microsoft YaHei"; padding: 20px; }}
                .back {{ color: #86a8e7; text-decoration: none; }}
                .container {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <a href="/" class="back">← 返回首页</a>
            <div class="container">
                <h2>环境监测模块</h2>
                <p>这里是环境监测相关内容</p>
            </div>
        </body>
    </html>
    """


@app.route('/canteen')
def canteen():
    return f"""
    <html>
        <head>
            <title>食堂管理</title>
            <style>
                body {{ font-family: "Microsoft YaHei"; padding: 20px; }}
                .back {{ color: #86a8e7; text-decoration: none; }}
                .container {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <a href="/" class="back">← 返回首页</a>
            <div class="container">
                <h2>食堂管理模块</h2>
                <p>这里是食堂管理相关内容</p>
            </div>
        </body>
    </html>
    """


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)