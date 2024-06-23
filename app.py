import streamlit as st
from streamlit_option_menu import option_menu 
#import about
import Aiobjectdetect
import NPKcoba,chatbotD2
#import stucture

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

with st.sidebar:
    st.title("App Menu")
    selected = option_menu(None, ["🏠 Home", '🔍 AI Object Detection',"👍 NPK Predictions", "💬 Monitor Soil Acidity"],
                           icons=[None], menu_icon=None, default_index=0
    )
st.sidebar.success("Select a demo above.")

if selected == '🏠 Home':
        st.write("# Welcome to Worm AI App! 👋")
        st.write("This is a final project for DigiLabs 2024 - Artificial Intelegent for Singapore International Foundation.")
        st.title("About The Project App")
        st.markdown('''This app helps you monitor the health of your worms in a compost soil tank. It uses computer vision to identify objects in the tank.
                    Also there is a feature to predicts the levels of Nitrogen (N), Phosphorus (P), and Potassium (K) - the three main nutrients for healthy worm growth (NPK). 
                   The app can provides recommendations on how much and what type of food to give your worms to keep them thriving through a chatbot interface.
                    ''')
        st.title("About The Dataset")
        st.write("- :blue[Images:] A collection of images captured from the compost soil tank, possibly containing worms, food scraps, and other elements. These images would be used to train the computer vision model for object detection.")
        st.write("- :blue[NPK data:] This data is likely numerical and would be used to train the model to predict NPK content.")
        st.write("- :blue[Monitor Soil Acidity:] Text data with recommendations on how much and what type of food to provide the worms")
        st.write("---")
        
elif selected== '🔍 AI Object Detection':
         Aiobjectdetect.run()
elif selected== '👍 NPK Predictions':
         NPKcoba.run()
else:
        chatbotD2.run()