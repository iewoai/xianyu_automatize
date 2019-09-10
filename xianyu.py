from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, datetime

desired_caps = {
		"deviceName": "Smartisan Pro2s",
		"platformName": "Android",
		"platformVersion": "8.1.0",
		"appActivity": "com.taobao.fleamarket.home.activity.MainActivity",
		"appPackage": "com.taobao.idlefish",
		"newCommandTimeout" : 900,# 防止过早退出应用，超时时间设置为10分钟
		"noSign": True,
		"noReset": True
		}

my_xpath = "//*[@resource-id='com.taobao.idlefish:id/tab_title'][@text='我的']"
# fabude_xpath = '//*[contains(@text, "我发布的")]'
fabude_xpath = '//android.view.View[contains(@text, "我发布的")]'
fabu_back_xpath = '//android.widget.FrameLayout[@content-desc="返回"]'
caliang_xpath = '//android.view.View[@content-desc="擦亮"]'
yicaliang_xpath = '//android.view.View[@content-desc="已擦亮"]'
shouxialibao_xpath = '//android.view.View[@content-desc="收下礼包"]'
xianyubi_queren_xpath = '//android.view.View[@content-desc="确认"]'
quqiandao_xpath = '//android.view.View[contains(@text, "签到")]'
qiandao_back_xpath = '//android.view.View[@content-desc="闲鱼币"]/../android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.ImageView'
qiandao_xpath = '//android.view.View[@content-desc="马上签到"]'
yiqiandao_xpath = '//android.view.View[@content-desc="已签到"]'

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
	# print(x, y)
	return (x, y)

# 向上滑屏幕
def swipeUp(t):
	l = getSize()
	# x坐标
	x1 = int(l[0] * 0.5)
	# 起始y坐标
	y1 = int(l[1] * 0.80)
	# 终点y坐标
	y2 = int(l[1] * 0.20)
	driver.swipe(x1, y1, x1, y2,t)

print("正在打开闲鱼app————————")
wait(my_xpath)


print('正在切换<我的>页面————————')
my = driver.find_element_by_xpath(my_xpath)
my.click()
wait(fabude_xpath)

# 切换到我的界面时检测是否签到，未签到则签到
if is_element_exist(quqiandao_xpath):
	print('今日未签到————————')
	driver.find_element_by_xpath(quqiandao_xpath).click()
	print('正在进入<签到>界面————————')
	wait(qiandao_xpath)
	qiandao = driver.find_element_by_xpath(qiandao_xpath)
	qiandao.click()
	time.sleep(0.2)
	if is_element_exist(shouxialibao_xpath):
		print('收下礼包————————')
		driver.find_element_by_xpath(shouxialibao_xpath).click()
		time.sleep(0.2)
	print('签到成功————————')
	driver.find_element_by_xpath(qiandao_back_xpath).click()
	wait(fabude_xpath)

print('今日已签到————————')


print('正在切换<我发布的>页面————————')
fabude = driver.find_element_by_xpath(fabude_xpath)
fabude.click()
wait(fabu_back_xpath)

# 检测每一个发布的宝贝，统计数据（浏览和想要），一天记录一次
# 若未擦亮则擦亮，每隔五分钟擦亮一个；若擦亮需要闲鱼币则消耗闲鱼币
# 签到操作

# 滑动后检查最后一个已擦亮的坐标是否变化，若无变化则停止滑动
def detect_loac():
	yicaliang = driver.find_elements_by_xpath(yicaliang_xpath)
	caliang = driver.find_elements_by_xpath(caliang_xpath)
	print('已擦亮个数：%d' % len(yicaliang))
	print('待擦亮个数：%d' % len(caliang))

	if len(yicaliang) != 0:
		return yicaliang[-1].location
		# size为元素大小
		# print(yicaliang[-1].size)
		# location为元素坐标值
		# print(yicaliang[-1].location)
	else:
		return caliang[-1].location

def get_caliang():
	caliang = driver.find_elements_by_xpath(caliang_xpath)
	if len(caliang) != 0:
		print('检测到%d个可以擦亮的宝贝————————' % len(caliang))
		for i in range(len(caliang)):
			# 出现除第一个外，其他几个擦亮定位在浏览上的错误，并未清楚错误如何触发
			print('正在擦亮第%d个宝贝————————' % (i + 1))
			# 永远点击擦亮中的第一个，来避免错误
			driver.find_elements_by_xpath(caliang_xpath)[0].click()

			# 判断是否需要闲鱼币
			if is_element_exist(xianyubi_queren_xpath):
				driver.find_element_by_xpath(xianyubi_queren_xpath).click()
			time.sleep(0.2)

			if len(driver.find_elements_by_xpath(caliang_xpath)) == len(caliang) - 1 * (i + 1):
				print('擦亮成功————————')
			else:
				print('擦亮失败————————')

			print('sleep五分钟————————')
			# 获得当前时间
			now = datetime.datetime.now()
			# 转换为指定的格式
			nowTime = now.strftime("%Y-%m-%d_%H:%M:%S")
			print('当前时间：%s' % nowTime)

			# 睡眠时间过长导致屏幕灰屏(接近五分钟)，导致后续操作失败，因此在长时间休眠后需要一次点击唤醒屏幕(默认设置为点击屏幕中央)
			# 若未熄灭点击中心区域可能带来一定风险，因此坐标改为无效区域，如顶端“我发布的”[441,72][637,153]
			time.sleep(5*60)
			driver.tap([(441, 72), (637, 153)], 100)
			# time.sleep(5)

get_caliang()
while True:
	loc_before = detect_loac()
	print('正在滑动屏幕————————')
	swipeUp(1000)
	loc_after = detect_loac()

	print('滑动前的坐标：')
	print(loc_before)
	print('滑动后的坐标：')
	print(loc_after)

	get_caliang()
	if loc_before == loc_after:
		print('滑到底部，停止滑动————————')
		break
print('全部擦亮完毕————————')
driver.quit()