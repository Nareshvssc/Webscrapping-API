import driver_launcher
from bs4 import BeautifulSoup as bs
import auxillary_fun
import clickbutton
import logger_courseinfo

def extract_info(filter_type,speci_course_name):
    path="https://courses.ineuron.ai"
    url = path+speci_course_name
    struc_info={}
    struc_info['Type']=filter_type
    try:
        driver = driver_launcher.driver_launchfun(url)
        page = driver.page_source
        page_bs = bs(page, "html.parser")
    except Exception as err:
        logger_courseinfo.logging_error(str(err)+"The page is not found")
    try:
        y = page_bs.find('section',{'class': 'Hero_hero__1u4sc'})
        struc_info['course_name'] = y.h3.text
    except Exception as err:
        struc_info['course_name']='Not found'
        logger_courseinfo.logging_error(f"assining None to {filter_type}")
    try:
        x = y.find('div',{'class':'Hero_course-desc__26_LL'})
        struc_info['course_description'] = x.text
    except Exception as err:
        struc_info['course_description'] = "Not found"
        logger_courseinfo.logging_error(f"assining None to course_description in {filter_type}")
    try:
        struc_info['job_gaurantee'] = y.find('div',{'class':'Hero_job-guarantee__1hKB0'}).a.text
    except Exception as err:
        struc_info['job_gaurantee'] ='No'
        logger_courseinfo.logging_info(f"assining None to job_gaurantee in {speci_course_name} "+str(err))
    try:
        start_page = page_bs.find('section',{'class':'CourseInfoLive_course-details__1xsWv'})
        struc_info['starts_time']= start_page.find('div',{'class':'CourseInfoLive_batch-details__3-13o'}).p.text
    except Exception as err:
        struc_info['starts_time']='Not available'
        logger_courseinfo.logging_info(f"assigning None to starts_time in {speci_course_name}"+str(err))

    try:
        skill_learned = start_page.find('div',{'class':'CourseLearning_card__WxYAo card'})
        w= skill_learned.findAll('li')
        struc_info['what_you_learned']=auxillary_fun.return_list_of(w)
    except Exception as err:
        struc_info['what_you_learned']='Not available'
        logger_courseinfo.logging_error(f"assigning None to what_you_learned in {speci_course_name}"+str(err))
    try:
        price_and_coursefeat = start_page.find('div',{'class':'CoursePrice_price-card__1_Bx- CoursePrice_card__C2Lr_ card'})
        struc_info['price'] = price_and_coursefeat.div.text
    except Exception as err:
        struc_info['price']=0
        logger_courseinfo.logging_error(f"assining None to price in {speci_course_name}"+str(err))

    try:
        course_features_page = price_and_coursefeat.find('div',{'class':'CoursePrice_course-features__2qcJp'})
        z= course_features_page.findAll('li')
        struc_info['course_features']=auxillary_fun.return_list_of(z)

    except Exception:
        struc_info['course_features']='NIL'
        logger_courseinfo.logging_error(f"assining None to course_features in {speci_course_name}")

    try:
        requirements_card = start_page.find('div',{'class':'CourseRequirement_card__3g7zR requirements card'})
        system_requirements_text = requirements_card.findAll('li')
        struc_info['system_requirement']=auxillary_fun.return_list_of(system_requirements_text)

    except Exception:
        struc_info['system_requirement']='NIL'
        logger_courseinfo.logging_info(f"assining None to system_requirement in {speci_course_name}")
    try:
        struc_info['course_structure'] = course_curicullum_extract(url,start_page)
    except Exception:
        struc_info['course_structure'] ='NIL'
        logger_courseinfo.logging_info(f"assining None to course_structure in {speci_course_name}")
    try:
        mentors_card = page_bs.findAll('div',{'class':'InstructorDetails_mentor__2hmG8 InstructorDetails_card__14MoH InstructorDetails_flex__2ePsQ card flex'})
        mentors_list=[]
        for i in range(len(mentors_card)):
            mentors_list.append((mentors_card[i].h5.text))
        struc_info['your_mentors']=mentors_list
        logger_courseinfo.logging_info(f"The scrapping of data for {speci_course_name} from {filter_type} type is completed")
    except Exception:
        struc_info['your_mentors']="NIL"
        logger_courseinfo.logging_info(f"assining None to mentors in {speci_course_name}")

    #converting list values of struc_info to string type before dumping in to csv
    struc_received = auxillary_fun.dico_covert_to_string(struc_info)
    return struc_received

    # print("the course name is = ",struc_received['course_name'],end='\n')
    # print(" course description = ", struc_received['course_description'],end='\n')
    # print("Program type by role = ",struc_received['job_gaurantee'])
    # print("start_date of programme= ",struc_received['starts_time'],end='\n')
    # print("what you will learn = ",struc_received['what_you_learned'],end='\n')
    # print("price of course = ",struc_received['price'])
    # print("COURSE FEATURES = ",struc_received['course_features'],end='\n')
    # print("System requirements for this = ",struc_received['system_requirement'],end='\n')
    # print("Course curicullum = ",struc_received['course_structure'])
    # print("mentors list = ",struc_received['your_mentors'])



def course_curicullum_extract(url,start_page):
    #url = "https://courses.ineuron.ai/Full-Stack-Data-Science-Bootcamp"
    driver = driver_launcher.driver_launchfun(url)
    view_more = start_page.find('span',{'class':"CurriculumAndProjects_view-more-btn__3ggZL"})
    #print(view_more)
    try:
        if view_more != None:
            view_button = driver.find_element_by_xpath('//*[@id="__next"]/section[2]/div/div/div[1]/div[3]/span')
            driver_mod = clickbutton.click_button(driver,view_button)
        else:
            driver_mod = driver
    except Exception as err:
        logger_courseinfo.logging_error(err)
    try:
        page = driver_mod.page_source
        page_html = bs(page, "html.parser")
        x = page_html.findAll('div', {'class': 'CurriculumAndProjects_accordion-header__3ALRY CurriculumAndProjects_flex__1-ljx flex'})
        course_curicullum = auxillary_fun.return_list_of(x)
    except Exception as err:
        logger_courseinfo.logging_error(err+"could not find course curriculum")
    driver.close()
    return course_curicullum




if __name__=='__main__':
    extract_info('Data-Science','/DSAR')

