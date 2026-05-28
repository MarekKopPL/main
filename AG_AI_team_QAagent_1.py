# Warning control
import warnings
warnings.filterwarnings('ignore')
from crewai import Agent, Task, Crew
import os
from utils import get_openai_api_key, get_openai_model_name
# Load environment variables
openai_api_key = get_openai_api_key()       
OPENAI_MODEL_NAME = get_openai_model_name()

print(openai_api_key)
print(OPENAI_MODEL_NAME)