import base64
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to encode the image
def encode_image(image_path):
    if type(image_path) == str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    else:
        return base64.b64encode(image_path.read()).decode("utf-8")


# Get image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
input_text = st.text_input("Input prompt", "Locate the open doors")
if uploaded_file:
    image = uploaded_file
else:
    image = "example/1534.png"

col1, col2 = st.columns(2)
col1.image(image)

base64_image = encode_image(image)


response = client.responses.create(
    model="gpt-5-mini",
    instructions="Output must be an image of the input image added with bounding boxes based on the request from the input text",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": input_text },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ],
   tools=[{"type": "image_generation"}] 
)

image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]
    with open("car_bbox.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
    col2.image("car_bbox.png")
else:
    # print(response.output)
    col2.markdown(response.output_text)