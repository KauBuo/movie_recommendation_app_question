import tkinter as tk  # tkinter库用于创建用户界面
import os # os库用于操作文件和目录
import pandas as pd  # pandas库用于数据处理
from sklearn.neighbors import KNeighborsClassifier  # sklearn库中的KNeighborsClassifier用于实现KNN算法
import numpy as np  # numpy库用于进行数值计算
import csv  # csv库用于读写csv文件
from PIL import Image, ImageTk  # PIL库用于处理图片
import logging  # logging库用于记录日志
import matplotlib.pyplot as plt  # matplotlib库用于数据可视化
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # matplotlib库中的FigureCanvasTkAgg用于在tkinter界面中显示matplotlib图像
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')  # 设置日志的输出格式和级别

class MovieRatingApp:  # 定义电影评分应用类
    def __init__(self, root):  # 初始化方法，设置应用的基本属性和界面
        self.root = root  # 设置应用的根窗口
        root.title("Movie Rating App")  # 设置应用的标题
        root.geometry("900x600")  # 设置应用的窗口大小

        # 加载并显示电影图片
        self.image1 = Image.open(os.path.join(os.path.dirname(__file__), 'post1_relie.jpg'))  # 加载电影1的图片
        self.image1.thumbnail((100, 300))  # 设置图片的大小
        self.movie1_image = ImageTk.PhotoImage(self.image1)  # 将图片转换为tkinter可以显示的格式
        self.movie1_label = tk.Label(root, image=self.movie1_image)  # 创建显示图片的标签
        self.movie1_label.grid(row=0, column=0, padx=10, pady=10)  # 将标签添加到界面上

        self.image2 = Image.open(os.path.join(os.path.dirname(__file__), "post2_family.jpg"))  # 加载电影2的图片
        self.image2.thumbnail((100, 300))  # 设置图片的大小
        self.movie2_image = ImageTk.PhotoImage(self.image2)  # 将图片转换为tkinter可以显示的格式
        self.movie2_label = tk.Label(root, image=self.movie2_image)  # 创建显示图片的标签
        self.movie2_label.grid(row=0, column=1, padx=10, pady=10)  # 将标签添加到界面上

        # 创建评分下拉菜单
        self.movie1_rating = tk.StringVar(root, value="1")  # 创建电影1评分的变量
        tk.OptionMenu(root, self.movie1_rating, "1", "2", "3", "4", "5").grid(row=1, column=0, padx=10, pady=10)  # 创建电影1评分的下拉菜单

        self.movie2_rating = tk.StringVar(root, value="1")  # 创建电影2评分的变量
        tk.OptionMenu(root, self.movie2_rating, "1", "2", "3", "4", "5").grid(row=1, column=1, padx=10, pady=10)  # 创建电影2评分的下拉菜单

        # 创建电影类型选择的单选按钮
        self.preference = tk.IntVar()  # 创建电影类型的变量
        tk.Radiobutton(root, text="动作片", variable=self.preference, value=0).grid(row=2, column=0, padx=10, pady=10)  # 创建选择动作片的单选按钮
        tk.Radiobutton(root, text="喜剧片", variable=self.preference, value=1).grid(row=2, column=1, padx=10, pady=10)  # 创建选择喜剧片的单选按钮

        # 创建按钮
        tk.Button(root, text="Confirm", command=self.confirm).grid(row=3, column=0, padx=10, pady=20)  # 创建确认按钮，点击后会调用confirm方法
        tk.Button(root, text="Clear", command=self.clear_plot).grid(row=3, column=1, padx=10, pady=20)  # 创建清除按钮，点击后会调用clear_plot方法
        tk.Button(root, text="Predict", command=self.predict_preference).grid(row=4, columnspan=2, padx=10, pady=20)  # 创建预测按钮，点击后会调用predict_preference方法
        self.predict_label = tk.Label(root, text="")  # 创建显示预测结果的标签
        self.predict_label.grid(row=5, columnspan=2, padx=10, pady=10)  # 将标签添加到界面上

        self.filename = os.path.join(os.path.dirname(__file__), 'ratings.csv')  # 设置存储评分数据的文件名

        if not os.path.isfile(self.filename):  # 如果文件不存在
            with open(self.filename, 'w', newline='') as file:  # 创建文件
                writer = csv.writer(file)  # 创建csv文件写入器
                writer.writerow(["Movie1", "Movie2", "Preference"])  # 写入表头

        # 创建显示图像的框架
        self.plot_frame = tk.Frame(root)  # 创建框架
        self.plot_frame.grid(row=0, column=2, rowspan=4, padx=10, pady=10)  # 将框架添加到界面上
        self.plot_ratings()  # 调用plot_ratings方法，显示评分数据的图像

    def confirm(self):  # 定义确认方法，用于保存用户的评分和电影类型选择
        m1_rating = self.movie1_rating.get()  # 获取电影1的评分
        m2_rating = self.movie2_rating.get()  # 获取电影2的评分
        preference = self.preference.get()  # 获取电影类型的选择

        with open(self.filename, 'a', newline='') as file:  # 打开文件
            writer = csv.writer(file)  # 创建csv文件写入器
            writer.writerow([m1_rating, m2_rating, preference])  # 写入用户的评分和电影类型选择

        self.plot_ratings()  # 调用plot_ratings方法，更新评分数据的图像

    def clear_plot(self):  # 定义清除方法，用于清除所有的评分数据
        with open(self.filename, 'w', newline='') as file:  # 打开文件
            writer = csv.writer(file)  # 创建csv文件写入器
            writer.writerow(["Movie1", "Movie2", "Preference"])  # 写入表头
        self.predict_label.config(text="")  # 清除预测结果的标签
        self.plot_ratings()  # 调用plot_ratings方法，更新评分数据的图像

    def plot_ratings(self):  # 定义显示评分数据的方法
        self.plot_frame.destroy()  # 销毁旧的框架, 因为需要重新绘制图像，否则会出现图像重叠的问题
        self.plot_frame = tk.Frame(self.root)  # 创建新的框架
        self.plot_frame.grid(row=0, column=2, rowspan=4, padx=10, pady=10)  # 将框架添加到界面上

        df = pd.read_csv(self.filename)  # 读取评分数据
        action_movies = df[df['Preference'] == 0]  # 获取动作片的评分数据
        comedy_movies = df[df['Preference'] == 1]  # 获取喜剧片的评分数据

        fig, ax = plt.subplots()  # 创建图像和坐标轴
        ax.grid(True)  # 显示网格
        ax.scatter(action_movies['Movie1'], action_movies['Movie2'], color='orange', label='Action')  # 绘制动作片的评分数据
        ax.scatter(comedy_movies['Movie1'], comedy_movies['Movie2'], color='blue', label='Comedy')  # 绘制喜剧片的评分数据

        # 把电影的坐标添加到图像上
        for i in range(len(action_movies)):
            ax.text(action_movies['Movie1'].iloc[i], action_movies['Movie2'].iloc[i], f'({action_movies["Movie1"].iloc[i]}, {action_movies["Movie2"].iloc[i]})', fontsize=8)
        for i in range(len(comedy_movies)):
            ax.text(comedy_movies['Movie1'].iloc[i], comedy_movies['Movie2'].iloc[i], f'({comedy_movies["Movie1"].iloc[i]}, {comedy_movies["Movie2"].iloc[i]})', fontsize=8)

        ax.set_xlabel('Movie A Rating')  # 设置x轴的标签
        ax.set_ylabel('Movie B Rating')  # 设置y轴的标签
        ax.set_xlim([0, 6])  # 设置x轴的范围
        ax.set_ylim([0, 6])  # 设置y轴的范围
        ax.legend()  # 显示图例

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)  # 将图像转换为tkinter可以显示的格式
        canvas.draw()  # 显示图像
        canvas.get_tk_widget().pack()  # 将图像添加到框架上

    def predict_preference(self):  # 定义预测方法，用于预测用户可能喜欢的电影类型
        df = pd.read_csv(self.filename)  # 读取评分数据
        X = df[['Movie1', 'Movie2']].values  # 从df中获取所有CSV文件中的评分数据
        y = df['Preference'].values  # 从df中获取所有CSV文件中的电影类型选择

        knn = KNeighborsClassifier(n_neighbors=1) # 创建KNN分类器, 设置K=1
        knn.fit(X, y)  # 训练分类器

        m1_rating = int(self.movie1_rating.get())  # 获取新用户对电影1的评分
        m2_rating = int(self.movie2_rating.get())  # 获取新用户对电影2的评分
        
        new_point = np.array([[m1_rating, m2_rating]])  # 创建用来做推理的新的数据点

        prediction = knn.predict(new_point) # 用 knn 预推理的数据点 new_point 的电影类型，0表示动作片，1表示喜剧片
        
        self.predict_label.config(text=f"给用户推荐的电影类型: {'动作片' if prediction[0] == 0 else '喜剧片'}")  # 显示预测结果

        self.plot_ratings()  # 调用plot_ratings方法，更新评分数据的图像

        plt.scatter(new_point[:, 0], new_point[:, 1], color='red', marker='x')  # 绘制新的数据点
        distances, indices = knn.kneighbors(new_point) # 获取新的数据点的最近邻的距离矩阵和索引值矩阵
        nearest_neighbor = X[indices[0][0]]  # 获取最近邻的坐标，这是一个列表，第一个元素是x坐标，第二个元素是y坐标
        plt.plot([new_point[0, 0], nearest_neighbor[0]], [new_point[0, 1], nearest_neighbor[1]], 'r--')  # 绘制从新的数据点到最近邻的虚线

root = tk.Tk()  # 创建tkinter的根窗口
app = MovieRatingApp(root)  # 创建电影评分应用
root.mainloop()  # 启动应用
