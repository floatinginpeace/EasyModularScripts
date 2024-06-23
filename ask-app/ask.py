import os
import sys
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

def main():
    ask_app_dir = os.getenv('EasyModularScriptsDir') + "/ask-app/"

    # Read the ASK_KEY environment variable
    ask_key = os.getenv('ASK_KEY')
    if not ask_key:
        print("Error: The ASK_KEY environment variable is not set.")
        sys.exit(1)
    client = Groq(api_key=ask_key)
    
    # Check if a prompt argument is provided
    if len(sys.argv) < 2:
        print("Usage: python ask.py <prompt>")
        sys.exit(1)

    # Combine the system prompt with the user prompt
    system_prompt = "Answer in as few characters as possible. No formatting tokens such as ` or ```"
    user_prompt = ' '.join(sys.argv[1:])
    combined_prompt = f"{system_prompt}\n{user_prompt}"
    
    try:
        # Make a request to Groq Llama 70b model in chat model
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user",
                 "content": f"{system_prompt}{user_prompt}"}
            ]
        )

        # Extract and print the response
        response_message = response.choices[0].message
        response_text = response_message.content
        print(response_text)

        # Save the response to the last_output.log file in the ask_app_dir dir
        if ask_app_dir:
            log_file_path = os.path.join(ask_app_dir, 'last_output.log')
            with open(log_file_path, 'w') as log_file:
                log_file.write(response_text)
        else:
            print("Error: The EasyModularScriptsDir environment variable is not set.")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
