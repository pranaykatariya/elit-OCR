try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
import requests
import re

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))
    # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

#Function to get prediction rate of tweet
def check_bullying(tweet):
    resp = requests.get('https://elit-hack.herokuapp.com/?query='+tweet)
    prediction = float(resp.text)

    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))

    return prediction

#to get image
extracted_text = (ocr_core('images/reply.PNG'))
lines = extracted_text.split('\n')
non_empty_lines = [line for line in lines if line.strip() != ""]
str_non_empty = ""
for line in non_empty_lines:
    str_non_empty += line+"\n"

data = str_non_empty.splitlines()
name = data[0]
user_id = data[1]
data.pop(0)
data.pop(0)
timestamp = data[-1]
data.pop(-1)
timestamp = timestamp.split("-")
time = timestamp[0]
date = timestamp[1]
platform = timestamp[2]
tweet = (" ".join(data))

#to get tagged username from tweet
result = re.findall("@([a-zA-Z0-9]{1,15})", tweet)
#calling above function by passing tweet
# prediction = check_bullying(tweet)
#add new api for posting data
post_url = 'http://cyber-bullying-api.herokuapp.com/api/report-create/'
email_url ='http://cyber-bullying-report.herokuapp.com/api/sendmail/1'
#if else for different prediction rate
if prediction>0.5:
    print ("bullying")
    print (tweet)
    from_user_id = user_id
    from_user = name
    to_user_id = result
    to_user = result
    time_now = timestamp
    #json object to add data to database
    details_object = {'complainer':"Null"
                    'abuser':from_user,
                    'victim':to_user,
                    'tweet':tweet,
                    'completed':"In progress"}
    #json object to send email
    email_object = {'from_user':from_user,
                    'from_user_id':from_user_id,
                    'to_user':to_user,
                    'to_user_id':to_user_id,
                    'bully_tweet':tweet,
                    #'location_bully':location_bully,
                    #'location_me':location_me,
                    'bully_rate':prediction,
                    'time_now':time_now,
                    'to':'pratikbansode2@gmail.com'}
    #calling to post data to database
    requests.post(url = url, data = details_object)
    #calling to send email
    #requests.post(url = email_url,data = email_object)
else:
    print ("not bullying")
    print(tweet)

print("Name:-", name)
print("User_ID:-", user_id)
print("Tweet:-", tweet)
print("Time:-", time)
print("Date:-", date)
print("Platform:-", platform)
