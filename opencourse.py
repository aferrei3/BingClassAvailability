
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import occreds
import os
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



dirname, filename = os.path.split(os.path.abspath(__file__))

start_time = time.time()


BU_BRAIN_URL = R"https://cas.cc.binghamton.edu/cas/login?service=https%3A%2F%2Fmy.binghamton.edu%2F"
BU_BRAIN_URL = R"https://ssb.cc.binghamton.edu/banner/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu&msg=\
WELCOME+Welcome+to+BU+BRAIN+Self+Service"

HWS_COURSES_URL = 'https://ssb.cc.binghamton.edu/banner/bwskfcls.P_GetCrse_Advanced'

GECKODIRVER = dirname + R"\geckodriver.exe"


BU_BRAIN_HOME_PAGE = R"https://ssb.cc.binghamton.edu/banner/twbkwbis.P_GenMenu?name=\
bmenu.P_MainMnu&msg=WELCOME+Welcome+to+BU+BRAIN+Self+Service"

REGISTRATION_PAGE = R"https://ssb.cc.binghamton.edu/banner/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu"




file = open('init.txt','r')
init_file_lines = file.read().splitlines()
term = init_file_lines[0]

init_file_lines.pop(0)
subjects = []
course_nums = []



for i in init_file_lines:
    x = i.split()
    

    subjects.append(x[0])
    course_nums.append(x[-1])







# options = Options()
# #options.headless = True
# driver = webdriver.Firefox(options=options, executable_path=GECKODIRVER)

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options, executable_path=GECKODIRVER)







def find_avail_classes(event = None, context = None):
    user = occreds.USERNAME
    user_pass = occreds.PASSWORD
#     options = Options()

#     driver = webdriver.Firefox(options=options, executable_path=GECKODIRVER)
 




    driver.get(BU_BRAIN_URL)

    username = driver.find_element_by_id("UserID")
    password = driver.find_element_by_name("PIN")

    username.send_keys(user)
    password.send_keys(user_pass)
    login_button = driver.find_element_by_xpath("/html/body/div[3]/form/p/input")
    login_button.click()





    # time.sleep(5)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/table[2]/tbody/tr[5]/td[2]/a")))
        
    finally:
        print('found')



    # print("poopoo")
    # sub = R"submenulinktext2" 
    # print(driver.page_source.encode("utf-8"))


    student_button = driver.find_element_by_xpath("/html/body/div[3]/table[2]/tbody/tr[5]/td[2]/a")
    student_button.click()

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a")))
    
    finally:
        print('found')
    


    registration_button = driver.find_element_by_xpath("/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a")
    registration_button.click()


    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/table[1]/tbody/tr[5]/td[2]/a')))
    
    finally:
        print('found')
    


    class_lookup = driver.find_element_by_xpath('/html/body/div[3]/table[1]/tbody/tr[5]/td[2]/a')
    class_lookup.click()


    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="term_input_id"]')))
    
    finally:
        print('found')
    


    pick_term = driver.find_element_by_xpath('//*[@id="term_input_id"]')
    pick_term.click()


    select = Select(driver.find_element_by_xpath('//*[@id="term_input_id"]'))

    select.select_by_visible_text(term)

    # try:
    #     element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/form/input[2]')))
    
    # finally:
    #     print('found')
    


    submit_button = driver.find_element_by_xpath('/html/body/div[3]/form/input[2]')
    submit_button.click()

    select = driver.find_element_by_xpath('//*[@id="subj_id"]')
    select.send_keys(Keys.CONTROL + Keys.ENTER)

    select = Select(driver.find_element_by_xpath('//*[@id="subj_id"]'))
    select.deselect_all()


   
    for subject in subjects:
        select.select_by_value(subject)

    submit = driver.find_element_by_xpath('/html/body/div[3]/form/span/input[1]')
    submit.click()


    # tbl = driver.find_element_by_xpath('/html/body/div[3]/form/div[2]/table').get_attribute('outerHTML')
    # df  = pd.read_html(tbl)
    # print(df)
    # p = df.read_table

    table_id = driver.find_element(By.XPATH, '/html/body/div[3]/form/div[2]/table')
    rows = table_id.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
    full_message = ''
    courses_avail = {}
    for row in rows:
        # Get the columns (all the column 2)        
        col = row.find_elements(By.TAG_NAME, "td") #note: index start from 0, 1 is col 2
        for i in range(len(course_nums)):
            if course_nums[i] in row.text and subjects[i] in row.text:
                for colu in col:
                    if col.index(colu) == 1:
                        crn = colu.text
                        

                
            
                        for colu in col:
                            if col.index(colu) == 12:
                                seats_avail = colu.text
                                full_message += subjects[i] + ' ' + course_nums[i] + ' has ' + seats_avail + ' available seats\n'
                                if int(seats_avail) > 0:
                                    courses_avail[subjects[i] + ' ' +course_nums[i]] = crn
    print(courses_avail)



    print(full_message)



    # for row in rows:
    #     # Get the columns (all the column 2)        
    #     col = row.find_elements(By.TAG_NAME, "td") #note: index start from 0, 1 is col 2
    #     for num in course_nums:
    #         if num in row.text:
    #             x = row.text.split()
    #             print(x)

    #     print(row.text) #prints text from the element


    # email = "dito.opencourses@gmail.com"

    # pas = "Goblin52"


    # sms_gateway = '5163821472@tmomail.net'
    # # The server we use to send emails in our case it will be gmail but every email provider has a different smtp 
    # # and port is also provided by the email provider.
    # smtp = "smtp.gmail.com" 
    # port = 587
    # # This will start our email server
    # server = smtplib.SMTP(smtp,port)
    # # Starting the server
    # server.starttls()
    # # Now we need to login
    # server.login(email,pas)

    # # Now we use the MIME module to structure our message.
    # msg = MIMEMultipart()
    # msg['From'] = email
    # msg['To'] = sms_gateway
    # # Make sure you add a new line in the subject
    # msg['Subject'] = "----CLASS AVAILABILITY----\n\n" 
    # # Make sure you also add new lines to your body
    # body = full_message
    # # and then attach that body furthermore you can also send html content.
    # msg.attach(MIMEText(body, 'plain'))

    # sms = msg.as_string()

    # server.sendmail(email,sms_gateway,sms)

    # # lastly quit the server
    # server.quit()

    # print("Took " + str(time.time() - start_time) + " seconds to run")





    return courses_avail




# find_avail_classes()














available_classes = find_avail_classes()

    




   


        




   





