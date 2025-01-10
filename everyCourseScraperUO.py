from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Course:
    def __init__(self, courseCode, courseName):
        self.courseCode = courseCode  
        self.courseName = courseName  
    
    def getCourseCode(self):
        return self.courseCode  
    
    def getCourseName(self):
        return self.courseName  


service = Service(executable_path=PUT_WEBDRIVER_PATH_HERE)
driver = webdriver.Chrome(service=service)

url = "https://catalogue.uottawa.ca/en/courses/"
driver.get(url)
driver.implicitly_wait(3)
htmlContent = driver.page_source
soup = BeautifulSoup(htmlContent, "html.parser")

filtered_links = []
for ul in soup.find_all("ul"):
    for li in ul.find_all("li"):
        a_tag = li.find("a")
        if a_tag and 'href' in a_tag.attrs and a_tag['href'].startswith("/en/courses/"):
            filtered_links.append(a_tag['href'])  
            
final_links = filtered_links[1:-1] 
allCourseLinks = [urljoin("https://catalogue.uottawa.ca", link) for link in final_links]

allCoursesHTMLContent = []
for link in allCourseLinks:
    driver.get(link)
    driver.implicitly_wait(3)
    htmlContent = driver.page_source
    allCoursesHTMLContent.append(htmlContent)

driver.quit()

allCoursesInfo = []
for html in allCoursesHTMLContent:
    soup = BeautifulSoup(html, "html.parser")
    
    courseblock_titles = soup.find_all("p", class_="courseblocktitle noindent")
    
    for courseblock in courseblock_titles:
        strong_tag = courseblock.find("strong")
        if strong_tag:
            allCoursesInfo.append(strong_tag.get_text(strip=True)) 

courses = []
for courseInfo in allCoursesInfo:
    
    courseName =""
    
    courseCode = courseInfo[:3]
    
    i = 3
    for char in courseInfo[4:]:
        i += 1
        if char.isdigit():
            courseCode += char +""
        else:
            
            break
    
    i += 1
    for char in courseInfo[i:]:
        if char != "(":
            courseName += char +""
        else:
            break
    courseName = courseName.strip()
    
    course = Course(courseCode, courseName)
    courses.append(course)

for course in courses:
    print(f"Course Code: {course.getCourseCode()}, Course Name: {course.getCourseName()}")
print(len(courses))