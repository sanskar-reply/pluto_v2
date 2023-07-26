from chat_prompts import predict_llm_output, generate_image
import concurrent.futures
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import streamlit as st
from streamlit_image_select import image_select

st.title('Pluto')

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

data = {
    "title": None,
    "caption": None,
    "color": None,
    "image": None,
}

st.input