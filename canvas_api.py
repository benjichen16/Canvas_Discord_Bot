import requests
import time
from datetime import datetime
import pytz

#auth2 workflow
#GET https://<canvas-install-url>/login/oauth2/auth?client_id=XXX&response_type=code&redirect_uri=https://example.com/oauth_complete&state=YYY&scope=<value_1>%20<value_2>%20<value_n>
# request = requests.get("https://canvas.ucsc.edu/login/oauth2/auth?client_id=%s&response_type=code&redirect_uri=https://canvas.ucsc.edu", os.getenv('CLIENT_ID'))
# print(request.json())

#curl -H "Authorization: Bearer <ACCESS-TOKEN>" "https://canvas.instructure.com/api/v1/courses"

class Canvas:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://canvas.instructure.com/api/v1/"
        self.headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json"
        }
    def get_courses(self):
        url = self.base_url + "courses"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_assignments(self):
        return_string = ""
        courses = self.get_courses()
        for course in courses:
            url = self.base_url + "courses/" + str(course["id"]) + "/assignments"
            assignments = requests.get(url, headers=self.headers).json()
            return_string = return_string + "Course: " + course["name"] + "\n"
            for assignment in assignments:
                if assignment["due_at"] != None:
                    assignment_due_date = datetime.strptime(assignment["due_at"], "%Y-%m-%dT%H:%M:%SZ")
                    if assignment_due_date.date() > datetime.now().date():
                        pst = pytz.timezone("US/Pacific")
                        date_time = pytz.timezone('UTC').localize(assignment_due_date)
                        date_time = date_time.astimezone(pst)
                        date_time = date_time.strftime("%m/%d/%Y %H:%M")
                        result = "Assignment: %s\nDue: %s" %(assignment["name"], date_time)
                        return_string = return_string + result
        return return_string

