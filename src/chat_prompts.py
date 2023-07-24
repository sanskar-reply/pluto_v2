from google.cloud import aiplatform
import vertexai
from vertexai.preview.language_models import TextGenerationModel
import openai
import os

#fetching the openai key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def predict_llm_output(
    project_id: str,
    model_name: str,
    temperature: float,
    max_decode_steps: int,
    top_p: float,
    top_k: int,
    content: str,
    location: str = "us-central1",
    tuned_model_name: str = "",
    ) :
    
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    if tuned_model_name:
      model = model.get_tuned_model(tuned_model_name)
    response = model.predict(
        content,
        temperature=temperature,
        max_output_tokens=max_decode_steps,
        top_k=top_k,
        top_p=top_p,
        )
    temp_var = response.text

    return temp_var

def generate_image(prompt):
    return openai.Image.create(
        prompt=prompt,
        n=3,
        size="256x256"
    )