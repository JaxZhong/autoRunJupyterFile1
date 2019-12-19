import os
import datetime
import uuid
from selenium import webdriver


driver = webdriver.PhantomJS(executable_path='D:\\tools\\phantomjs-2.1.1-windows\\bin\\phantomjs',service_args=['--load-images=no'],desired_capabilities=dcap)  # phantomjs的绝对路径
driver.set_window_size(CONFIG['WIDTH'], CONFIG['HEIGHT'])

filePath =  parentPath + '\\temp\\'+datetime.datetime.today().strftime('%Y%m%d_%H_%M_%S') +str(uuid.uuid1())
if not os.path.exists(filePath):
    os.makedirs(filePath)
imgPath = filePath + '\\HGReport.png'
driver.get("file:///" + htmlPath)