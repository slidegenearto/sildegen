from flask import Flask, render_template, request
import requests
import os
import urllib.request
from slide_gen.sendemail import send_email_with_attachment
from slide_gen.constants import email_subject,from_email,subject



from slide_gen import slidegen

app = Flask(__name__)


def download_file(url, save_folder, new_filename):
    try:
        os.makedirs(save_folder, exist_ok=True)
        urllib.request.urlretrieve(url,new_filename)
        return True
    except Exception as e:
        print("f Download Failed :{e}")
        return False


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
        # You can process/store the data here
        download_url=slidegen.mainfunction(company)
        print(download_url)
        filename=Folder_name+'/'+company+'.pptx'
        status=download_file(download_url['url'],Folder_name,filename)
        filepath=os.path.abspath(filename)
        status_code=send_email_with_attachment(from_email,email,subject,email_subject,filepath)

        return  render_template('index.html', email=email, company=company)
    
    return render_template('index.html', email=email, company=company)

if __name__ == '__main__':
    app.run(debug=True)
