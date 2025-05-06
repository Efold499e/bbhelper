import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from getpass import getpass

class bbhelper:
    id = 0
    password = ""
    driver = webdriver.Chrome()
    titles = ["作业", "ssignment", "omework"]
    def __init__(self, id, password, titles):
        self.id = id
        self.password = password
        self.titles = titles
        self.driver.implicitly_wait(3)
        self.driver.get('https://cas.sustech.edu.cn/cas/login?service=https://bb.sustech.edu.cn/webapps/bb-sso-BBLEARN/index.jsp')
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, '#username').send_keys(self.id)
        self.driver.find_element(By.CSS_SELECTOR, '#password').send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'][accesskey='l']").click()
        button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[id='agree_button']")))
        button.click()
    def get_homework(self):# roll_course()的子函数，用于具体获取作业操作，仅在roll_course()中调用
        try:
            homework = self.driver.find_element(By.CSS_SELECTOR, '#content_listContainer').text
            print(homework +'\n')
            self.driver.back()
            return homework
        except NoSuchElementException:
            print("没有找到作业喵~\n")
            self.driver.back()
            return None
    def roll_course(self):# 主要函数，用于遍历所有课程
        homework_dict = {}
        courses = self.driver.find_elements(By.CSS_SELECTOR,
            "a[href*='/webapps/blackboard/execute/launcher?type=Course'][target='_top']")
        len_courses = len(courses)
        for i in range(len_courses):
            time.sleep(1)
            courses = self.driver.find_elements(By.CSS_SELECTOR,
            "a[href*='/webapps/blackboard/execute/launcher?type=Course'][target='_top']")
            course = courses[i]
            course.click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//*[@id='menuPuller']").click()
            titles = self.titles
            time.sleep(1)
            course_name = self.driver.find_element(By.CSS_SELECTOR,"#courseMenu_link").text
            print(f"正在喵取 {course_name}的作业喵~\n")
            has_homework = 0
            for title in titles:
                homework_list = self.driver.find_elements(By.CSS_SELECTOR, f"span[title*='{title}']")
                time.sleep(0.5)
                self.driver.find_element(By.XPATH, "//*[@id='menuPuller']").click()
                if homework_list != []:
                    has_homework = 1
                    time.sleep(1)
                    if len(homework_list) != 1:
                        j = 0
                        for j in range(len(homework_list)):
                            self.driver.find_element(By.XPATH, "//*[@id='menuPuller']").click()
                            homework_list = self.driver.find_elements(By.CSS_SELECTOR, f"span[title*='{title}']")
                            homework_list[j].click()
                            homework = self.get_homework()
                            homework_dict[course_name] = homework
                    else:
                        self.driver.find_element(By.XPATH, "//*[@id='menuPuller']").click()
                        homework = homework_list[0].click() 
                        homework = self.get_homework()
                        homework_dict[course_name] = homework
                else:
                    continue
            if has_homework == 0:
                print(f"没有作业喵~\n")
            self.driver.back()
        return homework_dict
    def write_homework(self, homework_dict):# 用于将作业写入文件
        for course, homework in homework_dict.items():
            current_time = time.strftime("%Y-%m-%d", time.localtime())
            os.makedirs(f"./homework/{current_time}", exist_ok=True)
            with open(f"./homework/{current_time}/{course}_{current_time}.txt", "w", encoding="utf-8") as f:
                f.write(homework)
                print(f"已将{course}的作业写入文件{current_time}_{course}喵~\n")
        print("作业在homework文件夹下喵~\n")

    def close(self):
        print("喵取作业完成，正在退出浏览器喵~")
        self.driver.quit()

if __name__ == '__main__':
    login = json.load(open("login.json", "r", encoding="utf-8"))
    if login["id"] == "<Your SUSTech id>" or login["password"] == "<Your password>":
        print("欢迎使用bbhelper，首次使用请在终端键入您的学号和密码喵~")
        id = input("请输入您的学号：")
        password = getpass("请输入CAS密码（密码不显示，输入完按回车即可）：")
        json.dump({"id": id, "password": password, "titles": ["作业", "ssignment", "omework"]}, open("login.json", "w", encoding="utf-8"))
    else:
        print("欢迎使用bbhelper，已有登录信息，即将开始喵取作业喵~")
    print("请确认喵取作业title是否在titles中喵~\n")
    print("默认title有'作业'，'Assignment'，'Homework'喵~\n")
    print("如果有其他title，请在login.json中添加喵~\n")
    print("开始喵取作业喵~\n")
    titles = login["titles"]
    id = login["id"]
    password = login["password"]
    bb = bbhelper(id = id,password = password , titles = titles)
    homework_dict = bb.roll_course()
    bb.write_homework(homework_dict)
    bb.close()

