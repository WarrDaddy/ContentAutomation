# ContentAutomation

Automate the process of generating text content from images. By extracting text from the images, users can capture the main topics or keywords that the images represent, and then use those to generate relevant written content.

Prerequisites
OpenAI API Key - You can obtain this by following the instructions in this video - https://www.youtube.com/watch?v=nafDyRsVnXU 
Google's Vision API Key - Instructions can be found in this video. You can skip the step about creating a virtual environment. - https://www.youtube.com/watch?v=ddWRX2Y71RU&t=977s 
Scripts
The repository contains two scripts:

VisionAi_Text_Extraction.py - This script processes a batch of images, extracts text from each image using Google's Vision AI, and outputs the extracted text to a separate folder as .txt files.
Content_Generator.py - This script generates content based on extracted keywords, using OpenAI's GPT-3 model.
VisionAi_Text_Extraction.py
This script extracts text from a directory of images using Google Vision AI and outputs the extracted text to a .txt file in a separate directory.

How to Use:
Install the required Python libraries with pip install -r requirements.txt.
Place all the images you want to process in a single directory.
Run the script using python3 VisionAi_Text_Extraction.py.
On first run, you will be prompted to enter your Google Vision API key and the path to the directory containing the images. These will be stored in a configuration file (config_text_extraction.json) for future use.
Requirements:
Google Vision API key
A directory of images you want to process
Content_Generator.py
This script uses OpenAI's GPT-3 model to generate content based on keywords extracted from images. The keywords are stored as .txt files in an input directory. Each keyword set generates a separate piece of content, which is saved to an output directory.

How to Use:
Install the required Python libraries with pip install -r requirements.txt.
Run the script using python3 Content_Generator.py.
On first run, you will be prompted to enter your OpenAI API key and the path to the directory containing the .txt files. These will be stored in a configuration file (config_content_generator.json) for future use.
Requirements:
OpenAI API key
A directory of .txt files containing keywords to base content on

