import os
import course_info_extraction
import push_to_mongodb
import logger_courseinfo
import auxillary_fun

def page_text(course_name,username,password,data_base_name,collection_name):
    """to determine Course list under the main course_name at courses.ineuron.ai"""
    course_path= 'https://courses.ineuron.ai/category'
    url = os.path.join(course_path,course_name)
    page_bs = auxillary_fun.return_page_html(url)

    try:
        #x contains the names of the courses under the course_name
        x = page_bs.findAll("div",{"class":"Course_course-card__1_V8S Course_card__2uWBu card"})
        #doc_information is a varibale that keeps all documents in a list for mongodb
        #driver.close()
    except Exception as err:
        logger_courseinfo.logging_error(f"cannot found the courses in the {url }"+str(err))
    else:
        for i in range(len(x)):
            doc_information = course_info_extraction.extract_info(course_name,x[i].a['href'])
            logger_courseinfo.logging_info(f"The data has been sent for  pushing to mongodb for   for {x[i].a['href']}")
            push_to_mongodb.add_to_mongodb(doc_information,username,password,data_base_name,collection_name)
        #sending many documents of type course_name in mongodb


if __name__=='__main__':
    page_text('Marketing')
