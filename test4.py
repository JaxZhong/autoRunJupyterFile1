import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
import traceback
import os

if __name__ == '__main__':

    notebook_filename = "C:/Users/1/Desktop/abc.ipynb"
    # notebook_filename = "D:/jupyter/宏观团队/HG/1.高频跟踪/3.周度策略观点@/3.周度策略观点.ipynb"

    with open(notebook_filename,encoding='utf8') as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=1000, kernel_name='python3')

    try:
        out = ep.preprocess(nb, {'metadata': {'C:/Users/1/Desktop/': 'notebooks/'}})
        print("成功")
    except CellExecutionError as e:
        # out = None
        msg = '报告执行出错 "%s".\n' % notebook_filename
        msg += '请查看 "%s"' % 'C:/Users/1/Desktop/abc_123.ipynb'
        print(msg)
        print('-------------begin-------')
        exc = traceback.format_exc()
        print(exc.replace("\n","<br/>"))
        print('-------------end-------')
        with open('C:/Users/1/Desktop/abc_123.ipynb', mode='w', encoding='utf-8') as f:
            nbformat.write(nb, f)
    else:
        with open('C:/Users/1/Desktop/abc_123.ipynb', mode='w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        if (os.path.exists("C:/Users/1/Desktop/abc_123.html")):
            os.remove("C:/Users/1/Desktop/abc_123.html")
        os.system("jupyter nbconvert --to html --TemplateExporter.exclude_input=True  --TemplateExporter.exclude_output_prompt=True C:/Users/1/Desktop/abc_123.ipynb --output C:/Users/1/Desktop/abc_123.html")

    # print(nb.cells[0].outputs[0].text)
    print("dsadas")