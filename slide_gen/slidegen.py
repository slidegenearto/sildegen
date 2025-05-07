import requests
import time
from  .constants import SLIDE_GEN_KEY,OPEN_API_KEY,SLIDE_GEN_URL,STATUS_URL
from .prompt import prompt
import openai

openai.api_key=OPEN_API_KEY
api_key_slide=SLIDE_GEN_KEY
slide_gen_url=SLIDE_GEN_URL
prompt_eng=prompt

def slide_generator(data):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key_slide
    }
    payload = {
        "plain_text": data,
        "length": 10,
        "template": "default",
        "language": "ORIGINAL",
        "fetch_images": True,
        "tone": "professional",
        "verbosity": "text-heavy",  
        "custom_user_instructions":"do not repeat slides"
    }
    response = requests.post(slide_gen_url, headers=headers, json=payload).json()
    response_obj=dict(response)
    task_id=response_obj['task_id']
    print("taskid",task_id)
    download_url = STATUS_URL+task_id
    response = requests.get(download_url, headers=headers)
    responseObj=dict(response.json())
    print("responseObj",responseObj)
    status=responseObj["task_status"]
    while status != 'SUCCESS':
        time.sleep(4)
        response = requests.get(download_url, headers=headers)
        responseObj=dict(response.json())
        status=responseObj["task_status"]
        print("status",status)

    pptUrl=responseObj['task_result']
    return pptUrl

def data_generation(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']


def mainfunction(companyname):
    prompt=prompt_eng.format(companyname)
    generated_prompt=data_generation(prompt)
    print("Generated Prompts",generated_prompt)
    download_url=slide_generator(generated_prompt)
    return download_url

    



