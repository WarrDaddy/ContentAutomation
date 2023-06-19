# Import Modules
import os  # Import the os module
import openai
from types import SimpleNamespace
import json

# Load or initialize configuration
config_path = 'config_content_generator.json'
if os.path.exists(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
else:
    config = {
        'openai_api_key': input("Enter your OpenAI API key: "),
        'input_dir_path': input("Enter the path to the input directory: "),
    }
    with open(config_path, 'w') as file:
        json.dump(config, file)

# Validate that the provided input directory exists
assert os.path.exists(config['input_dir_path']), "The provided input directory does not exist."

# Authenticate API Key from configuration
openai.api_key = config['openai_api_key']

# Attempt a simple API request to check if the API key is valid
try:
    openai.Completion.create(engine="text-davinci-002", prompt="test", max_tokens=5)
except openai.api_errors.AuthenticationError:
    print("Invalid OpenAI API key.")
    exit(1)

# Set up models
models = {
    'text': {
        'best': 'text-davinci-002',  # Updated model names
        'better': 'text-curie-001',
        'good': 'text-babbage-001',
        'base': 'text-ada-001'
    }
}
models = json.loads(json.dumps(models), object_hook=lambda item: SimpleNamespace(**item))

# Output directory
output_dir_path = "Content_Output"

# Create the output directory if it does not exist
if not os.path.exists(output_dir_path):
    os.makedirs(output_dir_path)

# Define a function to execute OpenAI prompt
def generate_text(prompt=None, model=models.text.best):
    if prompt and not isinstance(prompt, str):
        prompt = str(prompt)
    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            temperature=1,  # if top_p is not 1.0, this should be 1.0
            max_tokens=150,
            top_p=1.0,  # if temperature is not 0, this should be 1.0
            frequency_penalty=0.2,
            presence_penalty=0.0,
        )
        return response
    except Exception as e:
        print(f"Error while generating text: {str(e)}")
        return None

# Run script
if __name__ == "__main__":
    # Directory path
    input_dir_path = config['input_dir_path']
    
    # List all files in directory
    files = os.listdir(input_dir_path)
    
    # Filter for .txt files
    txt_files = [f for f in files if f.endswith('.txt')]

    # For each txt file, read it, extract text, and generate a response
    for txt_file in txt_files:
        # Construct full file path
        input_file_path = os.path.join(input_dir_path, txt_file)
        
        # Open and read the file
        with open(input_file_path, 'r') as file:
            extracted_text = file.read()
        
        # Provide the prompt
        prompt = f"""
ChatGPT, as a health, wellness, and marketing expert, create a captivating and engaging Facebook post suitable for a health-conscious, mid-mature audience. The post should be based on the following information: '{extracted_text}'. 

Create an informative and engaging post that provides insights into healthy recipes, home cures, weight loss tips, and the healing powers of different types of tea. Encourage interaction, provide value to the audience, and spark curiosity about these health and wellness topics.

Consider using various strategies to increase engagement such as sharing a surprising fact about tea, asking an engaging question about their tea habits, or introducing a healthy recipe or home cure. And don't forget to sprinkle some relevant emojis 🍵💪 throughout the post where appropriate! The aim is to engage them with informative and inspiring content that can help them lead healthier lives.

Make sure to expand on the keywords that is provided. The response should be anywhere between 400-500 character for this facebook adpost.
"""
        response = generate_text(prompt)

        # Check if text was generated successfully
        if not response:
            continue

        # Output the response to a new file in the "Content-Output" directory
        # Replace spaces in the filename with underscores
        output_file_path = os.path.join(output_dir_path, txt_file.replace(' ', '_'))
        with open(output_file_path, 'w') as file:
            file.write(response.choices[0].text.strip())

        print(f"\nResponse for file: {txt_file}\n")
        print(response.choices[0].text.strip())
        print(f"Tokens used: {response['usage']['total_tokens']}\n")
