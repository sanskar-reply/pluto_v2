# Imports
from chat_prompts import predict_llm_output, generate_image
import concurrent.futures
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import streamlit as st
import chat_prompts
from streamlit_image_select import image_select
import time

# Define the title and description of the app
st.title('Pluto')
st.write('Recreating the gen ai app')

#sidebar to have instructions on how to use the app, have a tab
# with st.sidebar:
#     tab1, tab2, tab3 = st.tabs(["Instructions", "Contact Us", "Meet the Dev"])

#     with tab1:
#         st.header("How to use this app")
#         st.write("This section is under maintainence :construction:. Come back shortly")

#         with st.echo():
#             st.write("This code will be printed to the sidebar.")

#         # with st.spinner("Loading..."):
#         #     time.sleep(5)
#         # st.success("Done!")

#     with tab2:
#         st.header("Get in touch with the developers to report any bugs")
#         st.write("This section is under maintainence. Come back shortly")

#     with tab3:
#         st.header("Meet the Dev")
#         st.write("This section is under maintainence. Come back shortly")

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
image_1 = ""
image_2 = ""
image_3 = ""

data = {
    "title": None,
    "caption": None,
    "color": None,
    "image": None,
}

# Initialize the default app only if it's not initialized yet
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

# @st.cache_data(experimental_allow_widgets=False)
def get_titles(input_text):
    global title_list
    title_var = predict_llm_output("gen-ai-sandbox", "text-bison@001", 0.2, 256, 0.8, 40, intro_prompt + title_prompt + input_text,"us-central1", )
    lines = title_var.splitlines()
    for line in lines:
        title_list.append(line)
    # print(title_list)

    st.write(f'This was your input, {input_text}!')
    # title = st.selectbox(
    #     'Select one title from this list:',
    #     (title_list[0], title_list[1], title_list[2], title_list[3], title_list[4]))
    
    # st.text('You selected:' + title)

    return title_list

# @st.cache_data(experimental_allow_widgets=True)
def get_captions(input_text):
    global caption_list
    caption_var = predict_llm_output("gen-ai-sandbox", "text-bison@001", 0.3, 1024, 0.8, 40, intro_prompt + caption_prompt + input_text, "us-central1")
    lines = caption_var.splitlines()
    for line in lines:
        caption_list.append(line)
    # print(caption_list)

    # caption = st.selectbox(
    #     'Select one title from this list:',
    #     (caption_list[0], caption_list[1], caption_list[2], caption_list[3], caption_list[4]))
    
    # st.text('You selected:' + caption)

    return caption_list

# @st.cache_data(experimental_allow_widgets=True)
def get_images(input_text):
    global image_list
    global image_1
    global image_2
    global image_3
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
    # col1, col2, col3 = st.columns(3)
    
    # with col1:
    #    st.image(image_1["data"][0]["url"])
    # with col2:
    #    st.image(image_2["data"][0]["url"])
    # with col3:
    #    st.image(image_3["data"][0]["url"])

    # col4, col5, col6 = st.columns(3)

    # with col4:
    #    st.image(image_1["data"][1]["url"])
    # with col5:
    #    st.image(image_2["data"][1]["url"])
    # with col6:
    #    st.image(image_3["data"][1]["url"])
       
    # col7, col8, col9 = st.columns(3)

    # with col7:
    #    st.image(image_1["data"][2]["url"])
    # with col8:
    #    st.image(image_2["data"][2]["url"])
    # with col9:
    #    st.image(image_3["data"][2]["url"])

    # image = image_select(
    #     label="Select a picture",
    #     images=[image_1["data"][0]["url"], image_1["data"][1]["url"], image_1["data"][2]["url"], image_2["data"][0]["url"], image_2["data"][1]["url"], image_2["data"][2]["url"],image_3["data"][0]["url"], image_3["data"][1]["url"], image_3["data"][2]["url"]],
    #     use_container_width=False
    # )        

    return image_1, image_2, image_3

def select_titles(title_list):
    global title
    title = st.selectbox(
        'Select one title from this list:',
        (title_list[0], title_list[1], title_list[2], title_list[3], title_list[4]))
    
    st.text('You selected:' + title)

    return title

def select_captions(caption_list):
    global caption
    caption = st.selectbox(
        'Select one title from this list:',
        (caption_list[0], caption_list[1], caption_list[2], caption_list[3], caption_list[4]))
    
    st.text('You selected:' + caption)

    return caption

def select_images(image_1, image_2, image_3):
    global image
    image = image_select(
        label="Select a picture",
        images=[image_1["data"][0]["url"], image_1["data"][1]["url"], image_1["data"][2]["url"], image_2["data"][0]["url"], image_2["data"][1]["url"], image_2["data"][2]["url"],image_3["data"][0]["url"], image_3["data"][1]["url"], image_3["data"][2]["url"]],
        use_container_width=False
    )  

    return image

def do_something_with_the_selection_titles(title):
    data["title"] = title

def do_something_with_the_selection_captions(caption):
    data["caption"] = caption

def do_something_with_the_selection_image(image):
    data["image"] = image

def do_something_with_the_selection_color(color):
    data["color"] = color

# Step 3: Post data to Firestore
def post_to_firestore(collection_name, data):
    try:
        db = firestore.client()
        doc_ref = db.collection(collection_name).document()
        doc_ref.set(data)
        print(f"Data posted successfully to {collection_name}")
    except Exception as e:
        print(f"Error posting data: {e}")


with st.form("my_form"):
    input_text = st.text_input('Enter the product you would like to market:',)
    submitted = st.form_submit_button("Submit")
    if submitted:       
        # st.balloons()
        get_titles(input_text)
        st.write("titles generated")
        get_captions(input_text)
        st.write("captions generated")
        get_images(input_text)

color = st.color_picker('Pick A Color', '#00f900')
st.write('The current color is', color)
data["color"] = color

with st.form("Publish"):
    select_titles(title_list)
    select_captions(caption_list)
    select_images(image_1, image_2, image_3)
    st.write('Click publish to send results to the mobile app')
    published = st.form_submit_button("Submit")
    if published:
        do_something_with_the_selection_captions(caption)
        do_something_with_the_selection_color(color)
        do_something_with_the_selection_image(image)
        do_something_with_the_selection_titles(title)
        post_to_firestore('promotions', data)

"""
make a new container as a separate col on the side, update the image in there along with the title and the caption and colour when selections are made
Improve the prompts
Look into giving the user the ability to get more titles/captions/images
Add comments to the code
"""
