#!/usr/bin/python
# -- coding: utf-8 --
# author:未央



import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities





# 直接在初始化时指定路径
ser = Service(r'./msedgedriver.exe')
driver = webdriver.Edge(service=ser)
# 隐式等待最大时间为10秒
driver.implicitly_wait(10)
# 打开网页版雨课堂
driver.get('https://www.yuketang.cn/v2/web/index')
print("请在15秒时间内扫码登录雨课堂")
for i in range(15):
	time.sleep(1)


#将时间字符串转换为秒数，格式为 'HH:MM:SS
def time_to_seconds(time_str):
    """将时间字符串转换为秒数，格式为 'HH:MM:SS'"""
    parts = time_str.split(':')
    if len(parts) == 3:  # 确保有时、分、秒
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0
#点击”我听的课程“
tab_student_element = driver.find_element(By.ID,"tab-student").click()
#获取所有课程名称
class_name_list = []
class_element = driver.find_elements(By.CSS_SELECTOR,'div[class="el-card__body"]>div[class="left"] h1')
for class_name in class_element:
    class_name_list.append(class_name.text)
for i in range(len(class_name_list)):
    print(class_name_list[i],">>>>>>","课程代码:",i)
#将课程名称列表中的课程名称替换为课程代码
for class_id in range(len(class_name_list)):
    class_name_list[class_id]=class_id


i = int (input("请输入要学习的课程代码："))
#点击课程
class_name_click = class_element[i].click()
#点击展开获取课程列表
shuangjiantou_element=driver.find_element(By.CSS_SELECTOR,'div[class="sub-info"]>span>span>svg>use').click()
class_element=driver.find_elements(By.CSS_SELECTOR, 'div[class="el-tooltip activity-info"]')
print("课程列表个数:",len(class_element))
#获取课程列表
class_list=[]
class_text_list=[]
for class_number in range(len(class_element)):
    class_list.append(class_element[class_number])
for class_name in range(len(class_element)):
    class_text_list.append(class_element[class_name].text.split('\n'))
print(class_text_list)
for learning_class in class_list:
	# print(learning_class.text)
	#滚动到课程
	driver.execute_script("arguments[0].scrollIntoView(true);", learning_class)
	# 点击课程
	driver.execute_script("arguments[0].click();", learning_class)
	time.sleep(3)
	#获取课程名称
	name_elemnet_text=driver.find_element(By.CSS_SELECTOR,'span[class="text text-ellipsis"]').text
	html_content = driver.page_source
	# print(html_content)
	if "播放" in html_content:
		print("正在学习课程:", name_elemnet_text)
		#获取课程时长
		video_time = driver.find_element(By.CSS_SELECTOR, 'xt-time[class="xt_video_player_current_time_display fl"]')
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
			#静音设置倍速播放
			turn_sound = driver.find_element(By.CSS_SELECTOR, 'xt-icon[class="xt_video_player_common_icon"]').click()
			# print("静音设置完成")
			play_video = driver.find_element(By.CSS_SELECTOR, 'button[class="xt_video_bit_play_btn"]').click()


			# 二倍速播放这段代码借鉴的https://github.com/LetMeFly666/YuketangAutoPlayer不知道为什么自己定位到元素之后点击不了
			speedbutton = driver.find_element(By.TAG_NAME, 'xt-speedbutton')
			ActionChains(driver).move_to_element(speedbutton).perform()
			ul = speedbutton.find_element(By.TAG_NAME, 'ul')
			lis = ul.find_elements(By.TAG_NAME, 'li')
			li_speed2 = lis[0]
			diffY = speedbutton.location['y'] - li_speed2.location['y']
			for i in range(diffY // 10):  # 可能不是一个好算法
				ActionChains(driver).move_by_offset(0, -10).perform()
				time.sleep(0.3)
			time.sleep(0.5)
			ActionChains(driver).click().perform()
			print("二倍速播放设置成功")
			for play_time in tqdm(range(int(learning_time/2+4)),desc="正在学习"+name_elemnet_text):
				time.sleep(1)
			# time.sleep(10)


			print("课程已结束，正在返回")
			driver.back()

		else:
			print("该课程已完成")
			driver.back()
	else:
		print(name_elemnet_text,"该课程为作业，无需学习，请视频完成后自行处理。")
		driver.back()

print("所有课程学习完毕")






