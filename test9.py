import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
import traceback
import os

if __name__ == '__main__':

    notebook_filename = "C:/Users/1/Desktop/abc.ipynb"
    # notebook_filename = "D:/jupyter/宏观团队/HG/1.高频跟踪/3.周度策略观点@/3.周度策略观点.ipynb"

    os.system("jupyter nbconvert --ExecutePreprocessor.timeout=1000 --to notebook --execute C:/Users/1/Desktop/abc.ipynb --output C:/Users/1/Desktop/abc_123.ipynb")

    os.system("jupyter nbconvert --to html --TemplateExporter.exclude_input=True  --TemplateExporter.exclude_output_prompt=True C:/Users/1/Desktop/abc_123.ipynb --output C:/Users/1/Desktop/abc_123.html")

    # print(nb.cells[0].outputs[0].text)
    print("dsadas")