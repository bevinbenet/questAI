import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyCYnnjloPNvNbLYL1dQsfnGL2OiNyHJHx0")
generation_config = {
  "temperature": 1,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 5000,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

while True:
    prompt_parts =input("Enter the query:")
    response = model.generate_content(prompt_parts)
    print(response.text)
    response.candidates