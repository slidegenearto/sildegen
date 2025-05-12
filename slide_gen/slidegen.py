import requests
import time
from  .constants import SLIDE_GEN_KEY,OPEN_API_KEY,SLIDE_GEN_URL,STATUS_URL,perplexity_api_key,base_url
from .prompt import prompt
from openai import OpenAI

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
        "length": 1,
        "template": "default",
        "language": "ORIGINAL",
        "fetch_images": True,
        "tone": "professional",
        "verbosity": "text-heavy",  
        "custom_user_instructions":"Only include the exact text from the document, no extra information,Follow the instructions in the document very closely"
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
    """
    response = requests.get(download_url, headers=headers)
    pptUrl=responseObj['task_result'] """
    return response
    """
    while status != 'SUCCESS':
        time.sleep(4)
        response = requests.get(download_url, headers=headers)
        responseObj=dict(response.json())
        status=responseObj["task_status"]
        print("status",status)
    """

    """
    def data_generation(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return response['choices'][0]['message']['content']
    """

def data_generation(prompt,companyname):
    YOUR_API_KEY = "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"
    messages = [
        {
            "role": "system",
            "content": (
            prompt
            ),
        },
        {   
            "role": "user",
            "content": (
                companyname
            ),
        },
    ]
    client = OpenAI(api_key=perplexity_api_key, base_url=base_url)

    # chat completion without streaming
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    #print(response.choices)
    resp_dict=response.dict()
    print(resp_dict['choices'][0]['message']['content'])
    return resp_dict['choices'][0]['message']['content']


def mainfunction(companyname):
    #prompt=prompt_eng.format(companyname)
    prompt=prompt_eng.replace("(LOGO NAME)",companyname)
    generated_prompt=data_generation(prompt,companyname)
    #print("Generated Prompts",generated_prompt)
    response=slide_generator(generated_prompt)
    return response

    



