from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
'''
目标：
闲鱼自动擦亮宝贝
两种解决方案：
1.模拟器自登陆（失败，模拟器不能登陆淘宝）
2.fiddle抓包，躲避检测（失败，抓包导致模拟器第三方应用闪退；也没有找到有关appium自动登陆淘宝相关资料。）
3.真机自动化操作（实践成功）
结果：
目标达成
'''
desired_caps = {
				'platformName': 'Android',
				'deviceName': '127.0.0.1:7555',
				'platformVersion': '6.0.1',
				'appPackage': 'com.taobao.idlefish',
				'appActivity': 'com.taobao.fleamarket.home.activity.InitActivity',
				'unicodeKeyboard': True,
				'resetKeyboard': True,
				'noReset': True, 
				'fullReset': False,
				'noSign': True
				}
my_xpath = "//*[@resource-id='com.taobao.idlefish:id/tab_title'][@text='我的']"
user_name_id = "com.taobao.idlefish:id/aliuser_login_account_et"
user_password_id = "com.taobao.idlefish:id/aliuser_login_password_et"
login_id = "com.taobao.idlefish:id/aliuser_login_login_btn"
message_id = "com.taobao.idlefish:id/aliuser_login_switch_smslogin"
phone_id = "com.taobao.idlefish:id/aliuser_login_mobile_et"
send_phone_id = "com.taobao.idlefish:id/aliuser_login_send_smscode_btn"
name = "teacup12138"
password = ""
phone_number = ""

print("正在打开闲鱼app————————")
t0 = time.time()
try:
	driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
	wait_home = WebDriverWait(driver,20)
	wait_home.until(EC.presence_of_element_located((By.XPATH, my_xpath)))
	print("打开成功，消耗时间：%d秒" %(time.time()-t0, ))
except:
	print("打开失败，关闭webdriver")
	driver.quit()

my = driver.find_element_by_xpath(my_xpath)
print("正在登陆————————")
# 点击我的，sleep 0.1秒再登陆
my.click()
sleep(0.15)

# 直接输入用户名和密码失败，尝试短信验证登陆
'''
print("正在输入用户名————————")
user_name = driver.find_element_by_id(user_name_id)
user_name.clear()
user_name.send_keys(name)
sleep(0.1)

print("正在输入密码————————")
user_password = driver.find_element_by_id(user_password_id)
# 点击清除
user_password.click()
user_password.clear()

# tab清除
# driver.keyevent(61)

# keyevent清除密码框原有text
# 123移动光标至末尾
# driver.keyevent(123)
# user_passsword_text = user_password.get_attribute('text')
# for i in range(0,len(user_passsword_text)):
# 	# 67退格符
# 	driver.keyevent(67)

user_password.send_keys(password)
sleep(0.05)

print("正在点击登陆————————")
login = driver.find_element_by_id(login_id)
login.click()
'''
# 使用短信验证码登陆，手动输入验证码后点击登陆
print("正在使用短信验证码登陆————————")
message = driver.find_element_by_id(message_id)
message.click()

print("正在输入电话号码————————")
phone = driver.find_element_by_id(phone_id)
user_name.clear()
user_name.send_keys(phone_number)
sleep(0.1)

print("正在点击发送验证码————————")
send_phone = driver.find_element_by_id(send_phone_id)
user_password.click()

driver.quit()
