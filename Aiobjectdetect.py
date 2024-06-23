import streamlit as st
from roboflow import Roboflow
import cv2
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

def run():
    # Initialize the Roboflow object with the API key
    rf = Roboflow(api_key="D4hIkcJyjS0vwo23vXez")
    # Access the project and model
    project = rf.workspace("yoland").project("composed-worm-ai")
    model = project.version(1).model

    #col1, col2 = st.columns([1, 2])
    with st.sidebar:
        st.title("Configuration and Analysis")
        
        # Add sliders for confidence and overlap thresholds
        confidence_threshold = st.slider("Confidence Threshold", 0, 100, 40)
        overlap_threshold = st.slider("Overlap Threshold", 0, 100, 30)

        # Placeholder for analysis info
        analysis_info = []

# with col2:
    st.title("Ai Object Detection")
    st.markdown("""
    This page utilizes image recognition technology to help you identify objects in pictures. Upload an image, and I'll analyze it to provide a potential identification.
    """)
    
    uploaded_file = st.file_uploader("Insert the image", type=("jpg", "jpeg", "png"))

    if uploaded_file is not None:
        # Read the file as an image
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        # Convert image to RGB if it has an alpha channel
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Save the image temporarily to pass to the model
        image.save("temp_image.jpg")
        prediction = model.predict("temp_image.jpg", confidence=confidence_threshold, overlap=overlap_threshold).json()

        st.write("### Raw Prediction JSON")
        st.json(prediction)  # Display the raw prediction JSON for debugging

        # Draw the bounding boxes and labels on the image
        for pred in prediction['predictions']:
            x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']
            label = pred['class']
            confidence = pred['confidence']

            # Calculate the top-left and bottom-right points of the bounding box
            top_left = (int(x - w / 2), int(y - h / 2))
            bottom_right = (int(x + w / 2), int(y + h / 2))

            # Draw the bounding box with yellow color in BGR format
            cv2.rectangle(image_np, top_left, bottom_right, (0, 255, 255), 2)

            # Draw the label and confidence with blue color in BGR format
            label_text = f"{label} ({confidence:.2f})"
            cv2.putText(image_np, label_text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Add the information to the analysis list
            analysis_info.append({
                'Label': label,
                'Confidence': confidence,
                'Top-left': top_left,
                'Bottom-right': bottom_right
            })

        # Convert image back to RGB for displaying in Streamlit
        image_np_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

        # Display the image using Streamlit
        st.image(image_np_rgb, caption='Processed Image', use_column_width=True)

    # Display the analysis information as a table and heatmap
    if analysis_info:
        df = pd.DataFrame(analysis_info)

    #ith col1:
        st.write("### Detected Objects Analysis")
        st.write(df)

        st.write("### Confidence Levels Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(df.pivot_table(index='Label', values='Confidence', aggfunc='mean'), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

if __name__ == '__main__':
    run()
