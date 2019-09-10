from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time, re, datetime
import pandas as pd
import pickle

desired_caps = {
		"deviceName": "Smartisan Pro2s",
		"platformName": "Android",
		"platformVersion": "8.1.0",
		"appActivity": "com.taobao.fleamarket.home.activity.MainActivity",
		"appPackage": "com.taobao.idlefish",
		"newCommandTimeout" : 600,# 防止过早退出应用，超时时间设置为10分钟
		"noSign": True,
		"noReset": True
		}

my_xpath = "//*[@resource-id='com.taobao.idlefish:id/tab_title'][@text='我的']"
fabude_xpath = '//*[contains(@text, "我发布的")]'
# fabude_xpath = '//android.widget.ScrollView/android.view.View/android.view.View[6]'
fabu_back_xpath = '//android.widget.FrameLayout[@content-desc="返回"]'


baobei_xpath = '//android.widget.FrameLayout[contains(@content-desc, "价格")]'
baobei_back_xpath = '//*[@text="返回"]'
baobei_data_xpath = '//*[contains(@text, "担保交易")]'
t0 = time.time()

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


# 以xpath判断元素是否存在
def is_element_exist(xpath):
	try:
		time.sleep(0.2)
		driver.find_element_by_xpath(xpath)
		return True
	except:
		return False

# 以xpath等待元素加载
def wait(xpath):
	t0 = time.time()
	try:
		wait_home = WebDriverWait(driver,20)
		wait_home.until(EC.presence_of_element_located((By.XPATH, xpath)))
		print("打开成功，消耗时间：%d秒" %(time.time()-t0, ))
	except:
		print("打开失败，关闭webdriver")
		driver.quit()

# 获得机器屏幕大小x,y
def getSize():
	x = driver.get_window_size()['width']
	y = driver.get_window_size()['height']
	return (x, y)

# 向上滑
def swipeUp(t):
	l = getSize()
	# x坐标
	x1 = int(l[0] * 0.5)
	# 起始y坐标
	y1 = int(l[1] * 0.75)
	# 终点y坐标
	y2 = int(l[1] * 0.25)
	driver.swipe(x1, y1, x1, y2, t)

def detect(l):
	if len(l) != 0:
		return l[0]
	else:
		return 0

def detect_loac():
	baobei = driver.find_elements_by_xpath(baobei_xpath)
	return baobei[-1].location

print("正在打开闲鱼app————————")
wait(my_xpath)


print('正在切换<我的>页面————————')
my = driver.find_element_by_xpath(my_xpath)
my.click()
wait(fabude_xpath)

print('正在切换<我发布的>页面————————')
fabude = driver.find_element_by_xpath(fabude_xpath)
fabude.click()
wait(fabu_back_xpath)

print('正在统计宝贝数据————————')
datas = {}


while True:
	items = driver.find_elements_by_xpath(baobei_xpath)

	loc_before = detect_loac()
	print('滑动前的坐标：')
	print(loc_before)

	for item in items:
		title = item.get_attribute('name')
		title = title[:title.find('，')]
		
		if not title in datas.keys():
			print('第%d个宝贝————————' % (len(datas) + 1))
			print('正在统计<%s>的数据————————' % title)

			# 点击进入宝贝详情时可能出现未知错误，原因是出现提示导致点到提示或者降价、编辑
			try:
				driver.find_element_by_xpath('//android.widget.FrameLayout[contains(@content-desc,"%s")]//*[@content-desc="宝贝图片"]' % title).click()
			except NoSuchElementException:
				print('捕捉NoSuchElement异常：上滑100px')
				l = getSize()
				
				driver.swipe(int(l[0] * 0.5), int(l[1] * 0.75), int(l[0] * 0.5), int((l[1] * 0.75) - 100), 1000)

				driver.find_element_by_xpath('//android.widget.FrameLayout[contains(@content-desc,"%s")]//*[@content-desc="宝贝图片"]' % title).click()
			# item.click()
			wait(baobei_back_xpath)
			while True:
				swipeUp(2000)
				if is_element_exist(baobei_data_xpath):
					info = driver.find_element_by_xpath(baobei_data_xpath).get_attribute('text')
					want = detect(re.findall(r'(\d+)人', info))
					
					like = detect(re.findall(r'超赞(\d+)', info))

					look = detect(re.findall(r'浏览(\d+)', info))
					

					datas[title] = {
						'想要' : want,
						'超赞' : like,
						'浏览' : look
					}

					break
			driver.find_element_by_xpath(baobei_back_xpath).click()
			time.sleep(0.2)
	# 坐标滑动
	swipeUp(2000)

	# 元素滑动
	# driver.scroll(driver.find_elements_by_xpath('//*[@content-desc="宝贝图片"]')[-2], items[0], 2000)

	loc_after = detect_loac()
	print('滑动后的坐标：')
	print(loc_after)

	if loc_before == loc_after:
		print('滑到底部，停止滑动————————')
		break

print('统计结束————————')
driver.quit()

with open('xianyuData.p', 'wb') as f:
	print('开始储存————————')
	pickle.dump(datas, f)
	f.close()
print('储存成功————————')

def order_dict(sort_list, df):
	dict_after = {}
	for order in sort_list:
		if order in df.keys():
			dict_after[order] = df[order]
		else:
			dict_after[order] = {
						'想要' : 0,
						'超赞' : 0,
						'浏览' : 0
					}
	return dict_after

# datas = pickle.load(open('xianyuData.p', 'rb'))

sort_list = pickle.load(open('sort_list.p', 'rb'))

num = len(sort_list)
for i in datas.keys():
	if i not in sort_list:
		sort_list.append(i)
if num != len(sort_list):
	with open('sort_list.p', 'wb') as f:
		print('开始更新sort_list————————')
		pickle.dump(sort_list, f)
		f.close()
		print('更新成功————————')

print(len(sort_list))

# 获得当前时间

now = datetime.datetime.now()
# 转换为指定的格式
nowTime = now.strftime("%Y-%m-%d")
file_name = '%s.xlsx' % nowTime

print('正在保存为：%s' % file_name)

dict_after = order_dict(sort_list, datas)

# 写入excel
result_DF = pd.DataFrame(dict_after)
result_DF.T.to_excel(file_name)
print('保存成功，消耗时间：%d' % int(time.time() - t0))
