import os
from flask import Flask, render_template, request

# import our OCR function
from OCR_try import ocr_core 

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = ocr_core(file)
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
            time = ""
            try:
                time = timestamp[0]
            except:
                print('0')

            date = ""
            try:
                date = timestamp[1]
            except:
                print('1')
            
            platform = ""

            try:
                platform  = timestamp[2]
            except:
                print('2')
            tweet = (" ".join(data))

            #to get tagged username from tweet
            result = re.findall("@([a-zA-Z0-9]{1,15})", tweet)
            #calling above function by passing tweet
            # prediction = check_bullying(tweet)
            #add new api for posting data
            post_url = 'http://cyber-bullying-api.herokuapp.com/api/report-create/'
            email_url ='http://cyber-bullying-report.herokuapp.com/api/sendmail/1'
            #if else for different prediction rate
            
            print ("bullying")
            print (tweet)
            from_user_id = user_id
            from_user = name
            to_user_id = result
            to_user = result
            time_now = timestamp
            #json object to add data to database
            details_object = {'complainer':"Null",
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
            

            print("Name:-", name)
            print("User_ID:-", user_id)
            print("Tweet:-", tweet)
            print("Time:-", time)
            print("Date:-", date)
            print("Platform:-", platform)


            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()