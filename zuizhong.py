#!/usr/bin/python 
# -- coding: utf-8 --
# author:未央

import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import requests
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
import ddddocr


# 初始化 ddddocr 的滑块验证码匹配模型，禁用字符检测和OCR功能
ocr = ddddocr.DdddOcr(det=False, ocr=False)

def get_slide_width():
    # 背景图像路径
    bg_path = "slide_bg.png"

    # 打开并读取目标图像（滑块）文件
    with open('slide.png', 'rb') as f:
        target_bytes = f.read()

    # 打开并读取背景图像文件
    with open(bg_path, 'rb') as f:
        background_bytes = f.read()

    # 使用 ddddocr 进行滑块验证码匹配，获取匹配结果
    res = ocr.slide_match(target_bytes, background_bytes, simple_target=True)
    width = res.get('target')[0]
    # 打印匹配结果，res 是一个包含匹配位置等信息的字典
    return width

#将时间字符串转换为秒数，格式为 'HH:MM:SS
def time_to_seconds(time_str):
    """将时间字符串转换为秒数，格式为 'HH:MM:SS'"""
    parts = time_str.split(':')
    if len(parts) == 3:  # 确保有时、分、秒
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0

# 设置User-Agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

options = webdriver.EdgeOptions()
options.add_argument(f'user-agent={user_agent}')
# options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument('-headless=old')  # 启用无头模式
options.add_argument('--disable-gpu')	# 禁用GPU加速
options.add_argument("--incognito")
options.add_argument("--disable-extensions")  # 禁用扩展
# options.add_argument("--disable-gpu")  # 禁用GPU加速
options.add_argument("--no-sandbox")  # 运行沙箱模式
options.add_argument("--disable-dev-shm-usage")  # 禁用/dev/shm
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--log-level=3')

account = input("请输入雨课堂账号：")
# password = pwinput.pwinput(prompt="请输入雨课堂密码：", mask="*")
password=input("请输入雨课堂密码：")
print("注意: 请确保输入的账号和密码正确，本程序不会检测输入的账号和密码是否正确，直接进行验证码验证，验证码验证失败超过四次后，不建议继续验证，请等待1分钟后再次尝试。")
# 直接在初始化时指定路径
ser = Service(r'./msedgedriver.exe')
driver = webdriver.Edge(service=ser,options=options)
# 隐式等待最大时间为10秒
driver.implicitly_wait(10)
# 打开网页版雨课堂
driver.get('https://www.yuketang.cn/v2/web/index')
time.sleep(1)
change_account_login=driver.find_element(By.CSS_SELECTOR,'img[alt="账号密码登录"]').click()
accout=driver.find_element(By.CSS_SELECTOR ,'input[placeholder="输入手机号"]').send_keys(account)
password= driver.find_element(By.CSS_SELECTOR,'input[placeholder="输入密码"]').send_keys(password)
login_btn=driver.find_element(By.CSS_SELECTOR,'diV[class="submit-btn login-btn"]').click()
iframe_element=driver.find_element(By.ID ,'tcaptcha_iframe')
driver.switch_to.frame(iframe_element)
time.sleep(2)
# 滑动图片
slide_block = driver.find_element(By.ID, "slideBlock").get_attribute('src')
# 背景图片
slide_bg = driver.find_element(By.ID, "slideBg").get_attribute('src')
# 保存滑动图片
target_img = Image.open(BytesIO(requests.get(slide_block).content)).save(r'./slide.png')
# 保存背景图片
template_img = Image.open(BytesIO(requests.get(slide_bg).content)).save(r'./slide_bg.png')
# 获取滑块宽度
# time.sleep(2)
# 找到滑块
click_move = driver.find_element(By.ID, "tcaptcha_drag_thumb")

width = get_slide_width()
width = width * 340 / 680 - 27 - 27
# print("滑块宽度：" + str(width))

# 按照轨迹移动滑块
# 按住滑块
print("正在验证,请稍后...")
ActionChains(driver).click_and_hold(click_move).perform()

# print("第一次拖动滑块")
ActionChains(driver).move_by_offset(width, 0).perform()
time.sleep(2)
# 第二次拖动滑块
# 再往右滑动一个27像素的距离本身27像素的距离
# print("第二次拖动滑块")
ActionChains(driver).move_by_offset(27, 0).perform()
# time.sleep(3)
# 等待验证
time.sleep(1)
# 释放滑块
ActionChains(driver).release().perform()
time.sleep(2)


html = driver.page_source
# time.sleep(5)
# print(html)

while "拖动" in html:

	print("验证失败，重新加载验证码")
	driver.find_element(By.ID, "reload").click()
	time.sleep(0.3)
	# 滑动图片
	slide_block = driver.find_element(By.ID, "slideBlock").get_attribute('src')
	# 背景图片
	slide_bg = driver.find_element(By.ID, "slideBg").get_attribute('src')
	# 保存滑动图片
	target_img = Image.open(BytesIO(requests.get(slide_block).content)).save(r'./slide.png')
	# 保存背景图片
	template_img = Image.open(BytesIO(requests.get(slide_bg).content)).save(r'./slide_bg.png')
	# 获取滑块宽度

	# 找到滑块
	click_move = driver.find_element(By.ID, "tcaptcha_drag_thumb")

	width = get_slide_width()
	width = width * 340 / 680 - 27 - 27
	# print("滑块宽度：" + str(width))

	# 按照轨迹移动滑块
	# 按住滑块
	ActionChains(driver).click_and_hold(click_move).perform()

	# print("第一次拖动滑块")
	ActionChains(driver).move_by_offset(width, 0).perform()
	time.sleep(2)
	# 第二次拖动滑块
	# 再往右滑动一个27像素的距离本身27像素的距离
	# print("第二次拖动滑块")
	ActionChains(driver).move_by_offset(27, 0).perform()
	# time.sleep(3)
	# 等待验证
	time.sleep(1)
	# 释放滑块
	ActionChains(driver).release().perform()
	time.sleep(1)
	time.sleep(4)

else:
	print("登录成功")
	# time.sleep(1)
	driver.switch_to.default_content()
	# 点击”我听的课程“
	tab_student_element = driver.find_element(By.ID, "tab-student").click()
	# time.sleep(4)
	# 获取所有课程名称
	class_name_list = []
	class_element = driver.find_elements(By.CSS_SELECTOR, 'div[class="el-card__body"]>div[class="left"] h1')
	for class_name in class_element:
		class_name_list.append(class_name.text)
		# print(class_name.text)
	for i in range(len(class_name_list)):
		print(class_name_list[i], ">>>>>>", "课程代码:", i)
	# 将课程名称列表中的课程名称替换为课程代码
	for class_id in range(len(class_name_list)):
		class_name_list[class_id] = class_id

	i = int(input("请输入要学习的课程代码："))
	# 点击课程
	class_name_click = class_element[i].click()
	# 点击展开获取课程列表
	shuangjiantou_element = driver.find_element(By.CSS_SELECTOR, 'div[class="sub-info"]>span>span>svg>use').click()
	class_element = driver.find_elements(By.CSS_SELECTOR, 'div[class="el-tooltip activity-info"]')
	print("课程列表个数:", len(class_element))
	# 获取课程列表
	class_list = []
	class_text_list = []
	for class_number in range(len(class_element)):
		class_list.append(class_element[class_number])
	for class_name in range(len(class_element)):
		class_text_list.append(class_element[class_name].text.split('\n'))
	print(class_text_list)
	for learning_class in class_list:
		# print(learning_class.text)
		# 滚动到课程
		driver.execute_script("arguments[0].scrollIntoView(true);", learning_class)
		# 点击课程
		driver.execute_script("arguments[0].click();", learning_class)
		time.sleep(3)
		# 获取课程名称
		name_elemnet_text = driver.find_element(By.CSS_SELECTOR, 'span[class="text text-ellipsis"]').text
		html_content = driver.page_source
		# print(html_content)
		if "播放" in html_content:
			print("正在学习课程:", name_elemnet_text)
			# 获取课程时长
			video_time = driver.find_element(By.CSS_SELECTOR,'xt-time[class="xt_video_player_current_time_display fl"]')
			time.sleep(3)
			print("视频时长:", video_time.text.replace(' ', ''))
			time_start = video_time.text.split('/')[0]
			time_end = video_time.text.split('/')[1]
			# 转换为秒数
			start_seconds = time_to_seconds(time_start)
			end_seconds = time_to_seconds(time_end)
			# 计算剩余时间+5秒 方便结束课程
			learning_time = end_seconds - start_seconds
			# print(int(learning_time))
			if int(learning_time) > 0:
				print("需要学习时长:", learning_time, "秒")
				# 静音设置倍速播放
				turn_sound = driver.find_element(By.CSS_SELECTOR,'xt-icon[class="xt_video_player_common_icon"]').click()
				# print("静音设置完成")
				play_video = driver.find_element(By.CSS_SELECTOR, 'button[class="xt_video_bit_play_btn"]').click()
				# 二倍速播放这段代码借鉴的https://github.com/LetMeFly666/YuketangAutoPlayer不知道为什么自己定位到元素之后点击了没反应
				speedbutton = driver.find_element(By.TAG_NAME, 'xt-speedbutton')
				ActionChains(driver).move_to_element(speedbutton).perform()
				ul = speedbutton.find_element(By.TAG_NAME, 'ul')
				lis = ul.find_elements(By.TAG_NAME, 'li')
				li_speed2 = lis[0]
				diffY = speedbutton.location['y'] - li_speed2.location['y']
				for i in range(diffY // 10):  # 可能不是一个好算法
					ActionChains(driver).move_by_offset(0, -10).perform()
					time.sleep(0.2)
				time.sleep(0.3)
				ActionChains(driver).click().perform()
				print("二倍速播放设置成功")
				for play_time in tqdm(range(int(learning_time / 2 + 4)), desc="正在学习" + name_elemnet_text):
					time.sleep(1)
				# time.sleep(10)
				print("课程已结束，正在返回")
				driver.back()
			else:
				print("该课程已完成")
				driver.back()
		else:
			print(name_elemnet_text, "该课程为作业，无需学习，请视频完成后自行处理。")
			driver.back()
	print("所有课程学习完毕,正在关闭浏览器")
	time.sleep(3)
	driver.quit()
