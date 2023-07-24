# Imports
from chat_prompts import predict_llm_output, generate_image
import concurrent.futures
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import streamlit as st
import chat_prompts
from streamlit_image_select import image_select

# Define the title and description of the app
st.title('Pluto')
st.write('Recreating the gen ai app')

# Intro prompt to the language model
intro_prompt = '''
                    You are a professional prompt generator, Your most important skill is to generate and re-engineer the user prompts into a much more descriptive version of the initial input and return a version that would obtain the best output from a large language model like text bison and dall e while aligning to the constraint and category mentioned below:
                '''

# Title prompt to the language model
title_prompt = '''
                    Generate 5 catchy titles for marketing promotion ads. Make sure the title is longer than 5 words but no more than 10.

                    Do not include the category names in the output. Always use the number at the start of a sentence
                    User input:
                '''

# caption prompt to the language model
caption_prompt = '''
                    Generate 5 catchy captions for marketing promotion ad that would make people click on the ad instantly. Make sure the length is longer than 12 words but no more than 20.

                    Do not include the category names in the output. Always use the number at the start of a sentence
                    User input:
                '''

# image prompt to the language model
image_prompt = '''
                    Generate 5 image captions that would result in coloruful, vibrant marketing pictures. Use descriptive adjectives, and avoid animated pictures.

                    Do not include the category names in the output. Always use the number at the start of a sentence
                    User input:
                '''

title_list = []
caption_list = []
image_list = []

# @st.cache_data(experimental_allow_widgets=False)
def get_titles(input_text):
    title_var = predict_llm_output("gen-ai-sandbox", "text-bison@001", 0.2, 256, 0.8, 40, intro_prompt + title_prompt + input_text,"us-central1", )
    lines = title_var.splitlines()
    for line in lines:
        title_list.append(line)
    # print(title_list)

    st.write(f'This was your input, {input_text}!')
    title = st.selectbox(
        'Select one title from this list:',
        (title_list[0], title_list[1], title_list[2], title_list[3], title_list[4]))

    st.text('You selected:' + title)

    return title

# @st.cache_data(experimental_allow_widgets=True)
def get_captions(input_text):
    caption_var = predict_llm_output("gen-ai-sandbox", "text-bison@001", 0.3, 1024, 0.8, 40, intro_prompt + caption_prompt + input_text, "us-central1")
    lines = caption_var.splitlines()
    for line in lines:
        caption_list.append(line)
    # print(caption_list)

    st.cache_data()
    caption = st.selectbox(
        'Select one title from this list:',
        (caption_list[0], caption_list[1], caption_list[2], caption_list[3], caption_list[4]))

    st.text('You selected:' + caption)

    return caption

# @st.cache_data(experimental_allow_widgets=True)
def get_images(input_text):
    image_var = predict_llm_output("gen-ai-sandbox", "text-bison@001", 0.3, 1024, 0.8, 40, intro_prompt + image_prompt + input_text, "us-central1")
    lines = image_var.splitlines()
    for line in lines:
        image_list.append(line)
    # print(image_list)

    # Generationg images using OpenAI
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(generate_image, image_list[1])
        future2 = executor.submit(generate_image, image_list[2])
        future3 = executor.submit(generate_image, image_list[3])
        image_1 = future1.result()
        image_2 = future2.result()
        image_3 = future3.result()
    
    # #image bit
    # col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

    # with col1:
    #    st.image(image_1["data"][0]["url"])
    #    st.image(image_1["data"][1]["url"])
    #    st.image(image_1["data"][2]["url"])

    # with col2:
    #    st.image(image_2["data"][0]["url"])
    #    st.image(image_2["data"][1]["url"])
    #    st.image(image_2["data"][2]["url"])

    # with col3:
    #    st.image(image_3["data"][0]["url"])
    #    st.image(image_3["data"][1]["url"])
    #    st.image(image_3["data"][2]["url"])

    image = image_select(
        label="Select a picutre",
        images=[image_1["data"][0]["url"], image_1["data"][1]["url"], image_1["data"][2]["url"], image_2["data"][0]["url"], image_2["data"][1]["url"], image_2["data"][2]["url"],image_3["data"][0]["url"], image_3["data"][1]["url"], image_3["data"][2]["url"]],
    )

    return image 

# Step 3: Post data to Firestore
def post_to_firestore(collection_name, data, title, caption, image, color):
    # Initialize the Firebase Admin SDK
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)
    try:
        # Get a Firestore client instance
        db = firestore.client()
        # Reference to the document
        doc_ref = db.collection(collection_name).document()
        # Set the data to the document
        doc_ref.set(data)
        print(f"Data posted successfully to {collection_name}")
    except Exception as e:
        print(f"Error posting data: {e}")
    
    # Example data to post
    data = {
            'caption': caption,
            'cover_img': image,
            'theme_colour': color,
            'title': title,
        }

def get_color():
    color = st.color_picker('Pick A Color', '#00f900')
    st.write('The current color is', color)

def do_something_with_the_selection_titles():

    return 

def do_something_with_the_selection_captions():
    return

def do_something_with_the_selection_images():
    return

def do_something_with_the_selection_colors():
    return 

def main():
    with st.form("my_form"):
        input_text = st.text_input('Enter the product you would like to market:',)

        submitted = st.form_submit_button("Submit")
        if submitted:       
            # Call your set of functions here, passing the user_input
            st.text('Your input was:' + input_text)
            get_titles(input_text)
            get_captions(input_text)
            get_images(input_text)

    return input_text

if __name__ == "__main__":
    main()

"""
make a new container as a separate col on the side, update the image in there along with the title and the caption and colour when selections are made
"""
