from flask import Flask, render_template, request
import requests
import os
import urllib.request
from slide_gen.sendemail import send_email_with_attachment
from slide_gen.constants import email_subject,from_email,subject,SLIDE_GEN_KEY


key=SLIDE_GEN_KEY
from slide_gen import slidegen

app = Flask(__name__)


def download_file(url, save_folder, new_filename):
    try:
        os.makedirs(save_folder, exist_ok=True)
        urllib.request.urlretrieve(url,new_filename+'.pptx')
        return True
    except Exception as e:
        print("f Download Failed :{e}")
        return False

headers = {
       
    }
@app.route('/download',methods=["POST"])
def check_status():
    data= request.get_json()
    print(data)
    url=data.get('url')
    print("url",url)
    Folder_name="downloadppt"
    print("hello world......")
    with open("file.txt",'r') as f:
        textfile=f.read()
    fle=textfile.split(",")
    email=fle[1]
    company=fle[0]

    print("email",email)
    print("company",company)

    filename=Folder_name+'/'+company+'.pptx'
    print("filename",filename)
    status=download_file(url,Folder_name,company)
    print("status",status)
    filepath=os.path.abspath(company+'.pptx')
    print(filepath)
    
    status_code=send_email_with_attachment(from_email,email,subject,email_subject,filepath,company)
    print("status_code",status_code)
    return '{"status":"Success"}'

    """

    STATUS_URL = "https://api.slidespeak.co/api/v1/task_status/"
    headers = headers
    
    response = requests.get(STATUS_URL, headers=headers)
    """
    print("hello world")

    


Folder_name='downloadppt'
@app.route('/', methods=['GET', 'POST'])
def index():
    email = ""
    company = ""
    if request.method == 'POST':
        email = request.form.get('email')
        company = request.form.get('company')
        print(company)
        print(email)
        with open("file.txt",'w') as f:
            f.write(company+','+email)
        # You can process/store the data here
        response=slidegen.mainfunction(company)
        resp_obj=dict(response.json())


        """
        print(download_url)
        filename=Folder_name+'/'+company+'.pptx'
        status=download_file(download_url['url'],Folder_name,filename)
        filepath=os.path.abspath(filename)
        status_code=send_email_with_attachment(from_email,email,subject,email_subject,filepath,company)"""

        return  render_template('progress.html', TASK_ID=resp_obj['task_id'], TOKEN=key)
    
    return render_template('index.html', email=email, company=company)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
