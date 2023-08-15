# -*- coding:utf-8 -*-
import os.path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import zipfile
import string
from util.logger import log, base_path
from time import sleep
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains


def create_move_path(cur_x, cur_y, to_x, to_y):
    x, y = cur_x, cur_y
    if to_x - x == 0 and to_y - y == 0: return None
    result_path = []
    _move_x_offset, _move_y_offset = 0,0
    if abs(x - to_x) > abs(y - to_y):
        cs = abs(x - to_x)
    else:
        cs = abs(y - to_y)
    traj_x,traj_y = (to_x - x) / cs, (to_y - y) / cs
    _move_time,_random_time = 0,0
    _move_step = (16,20)
    move_step = random.randint(*_move_step)
    _random_tri = random.randint(3,6)  # 震动阈值
    while x != to_x and y != to_y:
        _move_time = _move_time + 1
        x,y = x + traj_x,y + traj_y
        if _move_time == move_step:
            _move_time, _random_time = 0, _random_time+1
            move_step = random.randint(*_move_step)
            #_move_delay = random.randint(10,15) / 1000 #移动间隔
            if _random_time == _random_tri:
                _move_x_offset = random.randint(-14,20) #x震动幅度
                _move_y_offset = random.randint(-10,10) #y震动幅度
                _random_time = 0
            result_path.append([x + _move_x_offset, y + _move_y_offset])
        elif abs(x - to_x) <= move_step and abs(y - to_y) <= move_step:
            result_path.append([to_x, to_y])
            x, y = to_x, to_y
    return result_path if len(result_path) > 0 else None


class ZpDriver(object):

    def __init__(self, headless=False, proxy=None, load_img=True):
        self.headless = headless
        self.proxy = proxy
        self.driver = self.get_chrome(load_img)
        self.timeout = 30
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.current_x = 0
        self.current_y = 0

    def __del__(self):
        """"""
        try:
            self.driver.quit()
            pass
        except:
            pass

    @classmethod
    def get_firefox(cls, headless=False, proxy=None):
        options = webdriver.FirefoxOptions()
        firefox_profile = webdriver.FirefoxProfile()
        if proxy:
            firefox_profile.set_preference("network.proxy.type", 1)
            firefox_profile.set_preference("network.proxy.http", proxy.split(":")[0])
            firefox_profile.set_preference("network.proxy.http_port", int(proxy.split(":")[1]))
            firefox_profile.set_preference("network.proxy.share_proxy_settings", True)
        options.set_preference("dom.webdriver.enabled",False)

        if headless:
            options.add_argument("--headless")
        # firefox_profile.set_preference("permissions.default.image", 2)
        # firefox_profile.set_preference("browser.migration.version", 9001)


        firefox_driver = webdriver.Firefox(options=options, firefox_profile=firefox_profile, executable_path='E:\driver\geckodriver.exe')

        # firefox_driver.maximize_window()
        return firefox_driver

    def get_chrome(self, load_img):
        options = webdriver.ChromeOptions()

        if self.proxy:
            if "@" in self.proxy:
                proxyHost, proxyPort, proxyUser, proxyPass = from_proxy_get_daili(self.proxy)
                proxy_auth_plugin_path = create_proxy_auth_extension(
                    proxy_host=proxyHost,
                    proxy_port=proxyPort,
                    proxy_username=proxyUser,
                    proxy_password=proxyPass)

                options.add_extension(proxy_auth_plugin_path)
            else:
                options.add_argument('--proxy-server=http://{}'.format(self.proxy))

        if load_img is False:
            options.add_argument('blink-settings=imagesEnabled=false')

        if self.headless:
            options.add_argument('--headless')
            options.add_argument("--window-size=1920, 1080")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        options.add_argument('--disable-gpu')           # 禁用GPU加速
        options.add_argument('--no-sandbox')
        options.add_experimental_option("detach", True)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('log-level=3')
        options.add_argument('--disable-blink-features=AutomationControlled')  # 谷歌浏览器去掉访问痕迹
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        chrome_driver = webdriver.Chrome(options=options)
        with open(os.path.join(base_path, 'data', 'stealth.min.js')) as f:
            js = f.read()

        chrome_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

        return chrome_driver

    def get_url(self, url):
        """打开网址并验证"""
        # self.driver.maximize_window()
        self.driver.set_page_load_timeout(60)
        count = 0
        while True:
            try:
                self.driver.get(url)
                self.driver.implicitly_wait(5)
                log.info("打开网页：%s" % url)
                return
            except TimeoutException:
                count += 1
                if count >= 3:
                    raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    def swtich_iframe(self, local):
        self.driver.switch_to.frame(self.find_element(local))

    def get_cookie(self):
        return self.driver.get_cookies()

    def scroll_into_view(self, js, ele):
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        time.sleep(0.5)

    def scroll_by_offset(self, length):
        self.driver.execute_script("window.scrollBy(0,{})".format(length))
        time.sleep(0.5)

    def input_single(self, locator, txt, clear=False):
        if clear:
            ele = self.find_element(locator)
            ele.clear()
        for t in txt:
            self.input_text(locator, t)
            sleep(random.uniform(0.05, 0.2))

    def input_text(self, locator, txt):

        """输入(输入前不清空)"""
        ele = self.find_element(locator)
        ele.send_keys(txt)

    def is_click(self, locator):
        """点击"""
        sleep(1)
        self.find_element(locator).click()

    def verify_element_present_by_xpath(self, xpath, wt=2):
        """验证元素是否存在"""
        try:
            self.driver.implicitly_wait(wt)
            if self.find_element(('xpath', xpath)) is None:
                return False
            return True
        except:
            return False

    def save_screen(self, filename):
        self.driver.save_screenshot(filename)

    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(name, value)

    def find_element(self, locator, wt=1):
        """寻找单个元素"""
        try:
            return ZpDriver.element_locator(lambda *args: WebDriverWait(self.driver, wt).until(
                EC.presence_of_element_located(args)), locator)
        except TimeoutException as e:
            return None

    def find_elements(self, locator):
        """查找多个相同的元素"""
        try:
            return ZpDriver.element_locator(lambda *args: self.wait.until(
                EC.presence_of_all_elements_located(args)), locator)
        except TimeoutException as e:
            return None

    def get_current_url(self):
        return self.driver.current_url

    def back(self):
        self.driver.back()

    def get_source(self):
        """获取页面源代码"""

        return self.driver.page_source

    def get_tracks2(self, distance):
        distance + 5
        '''
            拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
            变速运动基本公式：
            ① v=v0+at       匀加速\减速运行
            ② s=v0t+½at²    位移
            ③ v²-v0²=2as    
         '''
        # 初速度
        v0 = 0
        # 加减速度列表
        a_list = [50, 65, 80]
        # 时间
        t = 0.4
        # 初始位置
        s = 0
        # 向前滑动轨迹
        forward_stacks = []
        mid = distance * 3 / 5
        while s < distance:
            if s < mid:
                a = a_list[random.randint(0, 2)]
            else:
                a = -a_list[random.randint(0, 2)]
            v = v0
            stack = v * t + 0.5 * a * (t ** 2)
            # 每次拿到的位移
            stack = round(stack)
            if (s + stack) > distance:
                stack = distance - s + 5
            s += stack
            v0 = v + a * t
            forward_stacks.append(stack)
        back_stacks = [-5, ]
        return forward_stacks

    def get_tracks(self, distance):
        v = 0
        t = 0.2
        forward_tracks = []
        current = 0
        mid = distance * 4 / 5  # 减速阀值
        while current < distance:
            if current < mid:
                a = 2  # 加速度为+2
            else:
                a = -3  # 加速度-3
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))
        return forward_tracks

    def random_move(self):
        x = random.randint(100,800)
        y = random.randint(100,500)
        path = create_move_path(0,0,x,y)
        cur_x = 0
        cur_y = 0
        action = ActionChains(self.driver, duration=0)
        for x,y in path:
            action.move_by_offset(xoffset=x-cur_x, yoffset=y-cur_y).perform()
            cur_x = x
            cur_y = y
        self.current_x = x
        self.current_y = y

    def move_to(self, ele):
        ele_x = ele.location["x"] + 10
        ele_y = ele.location["y"] + 20
        print("滑块位置x:{} y:{}".format(ele_x, ele_y))
        path = create_move_path(0, 0, ele_x - self.current_x, ele_y - self.current_y)
        print(path)
        cur_x = 0
        cur_y = 0
        action = ActionChains(self.driver, duration=0)

        for x, y in path:
            action.move_by_offset(xoffset=x - cur_x, yoffset=y - cur_y)
            cur_x = x
            cur_y = y
        action.perform()
        self.current_x = ele_x
        self.current_y = ele_y

    def slide(self, distance, ele):
        # 移动鼠标到滑块
        self.move_to(ele)
        # 拖动滑块
        tracks = self.get_tracks(distance)
        print(tracks)
        print("滑动前鼠标位置x:{} y:{}".format(self.current_x, self.current_y))
        action = ActionChains(self.driver, duration=0)
        action.click_and_hold().perform()

        time.sleep(0.3)
        for tk in tracks:
            yoffset = random.randint(0, 2)
            action.move_by_offset(xoffset=tk, yoffset=yoffset)
            self.current_x += tk
            self.current_y += yoffset
        action.release()
        action.perform()
        print("滑动后鼠标位置x:{} y:{}".format(self.current_x, self.current_y))




def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password, scheme='http',
                                plugin_path=None):
    if plugin_path is None:
        plugin_path = os.path.join(base_path, 'data', r'{}_{}@http-dyn.dobel.com_9020.zip'.format(proxy_username, proxy_password))

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Dobel Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
            }
          };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


def from_proxy_get_daili(proxy):
    # proxy是这种格式 user:pass@ip:port
    user_pass_str, ip_port_str = proxy.split('@')
    proxyHost, proxyPort = ip_port_str.split(':')
    proxyUser, proxyPass = user_pass_str.split(':')
    return proxyHost, proxyPort, proxyUser, proxyPass
