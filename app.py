from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import logger_courseinfo
import pages_info
import push_to_mongodb
from flask import Flask, render_template, request
import driver_launcher
from flask_cors import cross_origin

app = Flask(__name__)
@app.route('/',methods=['GET']) #route to display home page for entering mongoDB credentials
#@cross_origin()
def homepage():
    return render_template("index.html")



@app.route('/scrapp_data',methods=['POST','GET']) #to display the data collected from website
#@cross_origin()
def index():
    if request.method =='POST':
        try:
            username = request.form['username']
            password = request.form['mypassword']
            data_base_name = request.form['DBname']
            collection_name = request.form['collec_name']
            if push_to_mongodb.check_mongo_db_login(username,password,data_base_name,collection_name):
                list_of_courses(username,password,data_base_name,collection_name)
            else:
                logger_courseinfo.logging_info("you entered the wrong details please check")
                return render_template("index.html")
        except Exception as err:
            logger_courseinfo.logging_info(err)
    else:
        return render_template("index.html")

def list_of_courses(username,password,data_base_name,collection_name):
    """!returns the list of courses in the website under the course tag"""
    task_url = "https://ineuron.ai"
    driver = driver_launcher.driver_launchfun(task_url)
    try:
        driver.get(task_url)
        driver.maximize_window()
        #time.sleep(delay)
        locate_course = driver.find_element(By.XPATH,'//*[@id="course-dropdown"]')
    except Exception as err_locate_course:
        logger_courseinfo.logging_error(str(err_locate_course)+" unable to find the the category in courses")
        driver.close()
    else:
        actions = ActionChains(driver)
        #hover the pointer to course button
        actions.move_to_element(locate_course)
        actions.perform()
        #Extract the courses once pointer hovers
    try:
        #variours list of courses captured when pointers over to courses in ineuron.ai
        element = [driver.find_element(By.XPATH,'//*[@id="categories-list"]/div').text]
    except Exception as err_course_list:
        logger_courseinfo.logging_error(err_course_list)
        driver.close()
    else:
        course_lists = element[0].split("\n")
        logger_courseinfo.logging_info("the courses found under course are "+str(course_lists))

    try:
        for course in course_lists:
            course = course.replace(" ",'-')
            pages_info.page_text(course,username,password,data_base_name,collection_name)

    except Exception:
        logger_courseinfo.logging_error("error getting courses from ineuron please check connection")
        driver.close()
    else:
        driver.close()

#how to run
#download the chromeinstalle.exe
#step1.check the logger and paste the http://127.0.0.1:5000/  in gogglechrome only
#step2. Enter details
#step3. username-Naresh  Password-Naresh123 , data_base_name = Ineuronwebscarpper_1   collection name = Full_website_data



if __name__=='__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    #list_of_courses()





