import threading
import os
import uuid

if __name__ == '__main__':

    # f = os.popen("jupyter nbconvert --ExecutePreprocessor.timeout=1000 --to notebook --execute D:\jupyter\宏观团队\HG/1.高频跟踪/1.周度宏观跟踪@/1.周度宏观跟踪.ipynb --output D:\projectFile\lrhg//userfiles/jupyter/1/1.周度宏观跟踪-20191216.ipynb")
    f = os.system("jupyter nbconvert --ExecutePreprocessor.timeout=1000 --to notebook --execute D:\jupyter\宏观团队\HG/1.高频跟踪/1.周度宏观跟踪@/1.周度宏观跟踪.ipynb --output D:\projectFile\lrhg//userfiles/jupyter/1/1.周度宏观跟踪-20191216.ipynb")
    d = f.read()  # 读文件
    print(type(d))
    print(d)
    f.close()

    # os.system(r"python %s/test.py > terminal_record.txt" %os.getcwd())