import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

# Load your models (replace with your actual loading logic)
with open('best_modelmor_save.pkl', 'rb') as file_1:
    best_modelmor = pickle.load(file_1)

# def classify_fertilizer(npk_values):
#     """
#     This function takes a DataFrame row containing NPK values for one sensor and classifies the fertilizer type.

#     Args:
#         npk_values (pd.Series): A Series containing NPK values (e.g., df.iloc[0] for the first sensor's row).

#     Returns:
#         str: The fertilizer type classification (e.g., "High NPK Fertilizer").
#     """
#     average_npk = npk_values.mean()
#     if average_npk > 0.7:
#         return "High NPK Fertilizer"
#     elif average_npk > 0.4:
#         return "Balanced NPK Fertilizer"
#     else:
#         return "Low NPK Fertilizer"

# def plot_fertilizer_distribution(df):
#     """
#     This function creates a pie chart showing the distribution of fertilizer types in the DataFrame.
#     """
#     fertilizer_counts = df['Fertilizer Type'].value_counts().sort_values(ascending=False)
#     fig, ax = plt.subplots(figsize=(8, 6))
#     ax.pie(fertilizer_counts, labels=fertilizer_counts.index, autopct="%1.1f%%")
#     ax.set_title("Distribution of Fertilizer Types")
#     ax.axis('equal')
#     st.pyplot(fig)

# def recommend_action(fertilizer_type, reference_study=None):
#     """
#     This function takes the fertilizer type and optionally a reference study for recommendations.

#     Args:
#         fertilizer_type (str): The fertilizer type classification (e.g., "High NPK Fertilizer").
#         reference_study (str, optional): A reference study for specific recommendations. Defaults to None.

#     Returns:
#         str: The recommended action based on fertilizer type and potentially the reference study.
#     """
#     base_message = "**Action:** Maintain current fertilization practices or adjust slightly based on specific plant needs and soil tests."

#     if reference_study is not None:
#         if fertilizer_type == "High NPK Fertilizer":
#             study_recommendation = "[Reference Study](link) suggests reducing nitrogen application by X% for crops like Y in soil conditions similar to yours."
#             return study_recommendation
#         elif fertilizer_type == "Balanced NPK Fertilizer":
#             return base_message
#         else:
#             study_recommendation = "[Reference Study](link) suggests increasing specific nutrients based on the identified deficiency. Consider a targeted fertilizer and consult an agronomist."
#             return study_recommendation

#     else:
#         if fertilizer_type == "High NPK Fertilizer":
#             return "**Action:** Reduce nitrogen application as the soil is already high in N. Consider using a fertilizer with a lower N-P-K ratio."
#         elif fertilizer_type == "Balanced NPK Fertilizer":
#             return base_message
#         else:
#             return "**Action:** Increase NPK application as the soil is deficient in nutrients. Consider using a fertilizer with a higher N-P-K ratio, but be mindful of over-fertilization."


# def recommend_plants(npk_ratio):
#     plants = {
#         "10:10:10": ["Tomatoes", "Flowering Plants", "Fruit Trees", "Herbs"],
#         "10:5:5": ["Leafy Greens"],
#         "5:10:10": ["Tomatoes", "Root Vegetables", "Flowering Plants"],
#         "10:20:10": ["Root Vegetables"],
#         "20:5:10": ["Grasses"],
#         "30:0:4": ["Grasses"],
#         "5:20:20": ["Legumes"]
#     }
#     return plants.get(npk_ratio, ["Unknown NPK ratio - please consult a specialist"])

# def recommend_action(npkratio01, npkratio02):
#     plants01 = recommend_plants(npkratio01)
#     plants02 = recommend_plants(npkratio02)
#     return f'For NPKratio01 ({npkratio01}): {", ".join(plants01)}; For NPKratio02 ({npkratio02}): {", ".join(plants02)}'

def normalize_npk_ratio(n, p, k):
    min_value = min(n, p, k)
    return f'{n / min_value * 10:.0f}:{p / min_value * 10:.0f}:{k / min_value * 10:.0f}'

def calculate_npk_ratio01(row):
    return normalize_npk_ratio(row["Nitrogen01"], row["Phosphorous01"], row["Potassium01"])

def calculate_npk_ratio02(row):
    return normalize_npk_ratio(row["Nitrogen02"], row["Phosphorous02"], row["Potassium02"])

def recommend_fertilizer(npk_ratio):
    fertilizer_recommendations = {
        "10.00:10.00:10.00": "Balanced fertilizer (10-10-10)",
        "10.00:5.00:5.00": "High nitrogen fertilizer (10-5-5) for leafy growth",
        "5.00:10.00:10.00": "Phosphorus and potassium-rich fertilizer (5-10-10) for root and fruit development",
        "10.00:20.00:10.00": "High phosphorus fertilizer (10-20-10) for root vegetables",
        "20.00:5.00:10.00": "High nitrogen fertilizer (20-5-10) for lawns",
        "30.00:0.00:4.00": "High nitrogen fertilizer (30-0-4) for grasses",
        "5.00:20.00:20.00": "Phosphorus and potassium-rich fertilizer (5-20-20) for legumes",
    }
    # Find the closest match in the recommendations dictionary
    closest_match = min(fertilizer_recommendations.keys(), key=lambda k: sum(abs(float(a) - float(b)) for a, b in zip(k.split(':'), npk_ratio.split(':'))))
    return fertilizer_recommendations.get(closest_match, "Unknown NPK ratio - please consult a specialist")

def recommend_action(npkratio01, npkratio02):
    fertilizer01 = recommend_fertilizer(npkratio01)
    fertilizer02 = recommend_fertilizer(npkratio02)
    return (f"For NPKratio01 ({npkratio01}) means {fertilizer01};\n For NPKratio02 ({npkratio02}) means {fertilizer02}")

def plot_npk_ratios(df):
    melted_df = pd.melt(df, id_vars=["NPKratio01", "NPKratio02", "Meaning"], 
                        value_vars=["Nitrogen01", "Phosphorous01", "Potassium01", "Nitrogen02", "Phosphorous02", "Potassium02"], 
                        var_name="Nutrient", value_name="Value")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=melted_df, x="Nutrient", y="Value", hue="Nutrient", ax=ax)
    ax.set_title("NPK Ratios with Meaning Fertilizer")
    
    for i, row in df.iterrows():
        ax.text(0.5, max(row[["Nitrogen01", "Phosphorous01", "Potassium01"]]) + 10, f'NPK01: {row["NPKratio01"]}\n{row["Meaning"].split(";")[0]}', ha='center', va='bottom', fontsize=0, color='black', bbox=dict(facecolor='white', alpha=0.5))
        ax.text(2.5, max(row[["Nitrogen02", "Phosphorous02", "Potassium02"]]) + 10, f'NPK02: {row["NPKratio02"]}\n{row["Meaning"].split(";")[1]}', ha='center', va='bottom', fontsize=0, color='black', bbox=dict(facecolor='white', alpha=0.5))
    
    st.pyplot(fig)


def run():
    st.title("NPK Prediction and Fertilizer")
    st.write("NPK fertilizer, it is an acronyms for N-Nitrogen, P-Phosphorus and K-Potassium. The combination may differ depending on the nutrients contains.")
    st.markdown(''':red[Nitrogen (N)] is needed for leaf growth and is responsible for making plants greener.
                   :green[Phosphorus (P)] promotes root development, which helps to anchor and strengthen plants.
                   :orange[Potassium (K)], also known as potash, helps the plant fight off diseases and keeps it vigorous, enabling it to withstand extreme temperatures and ward off disease.
                
                ''')
    st.write("This tool predicts the levels of Nitrogen (N), Phosphorus (P), and Potassium (K) - crucial nutrients for plants. It then give you the meaning of the right fertilizer, ensuring your crops have what they need to thrive and reach their full potential.")
    st.write("### Choose your preferred method for data input:")
    data_option = st.selectbox("Select Input Method", ["Upload CSV File", "Manual Input"])
    st.write("---")

    with st.sidebar:
        st.title("NPK Prediction")

    if data_option == "Upload CSV File":
        sample_data = {
            'Light Intensity': [1000, 1500],
            'Temp01': [25, 30],
            'Hum01': [50, 60],
            'Heat01': [20, 25]}
        sample_df = pd.DataFrame(sample_data)
        csv = sample_df.to_csv(index=False)
        st.download_button(
            label="Download Sample CSV",
            data=csv,
            file_name='sample_data.csv',
            mime='text/csv'
        )

        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file is not None:
            if st.button("Predict"):
                df = pd.read_csv(uploaded_file)
                predictions = best_modelmor.predict(df)
                targets = ['Phosphorous01', 'Phosphorous02', 'Nitrogen01', 'Nitrogen02', 'Potassium01', 'Potassium02']

                for i, target in enumerate(targets):
                    df[target] = predictions[:, i]

                df["NPKratio01"] = df.apply(calculate_npk_ratio01, axis=1)
                df["NPKratio02"] = df.apply(calculate_npk_ratio02, axis=1)

                df["Meaning"] = df.apply(lambda row: recommend_action(row["NPKratio01"], row["NPKratio02"]), axis=1)
                df2 = df[['NPKratio01', 'NPKratio02','Meaning']].copy()
                
                st.write(df2)
                st.success("Predictions and Recommendation Action added to your data!")
                plot_npk_ratios(df.copy())       
                
        else:
            st.info("Upload a CSV file to get started.")

    elif data_option == "Manual Input":

        st.write("### Insert data based on the form information")
        data = {}
        for key in ['Light Intensity', 'Temp01', 'Hum01', 'Heat01']:
            data[key] = st.number_input(key)
        df = pd.DataFrame(data, index=[0])

        if st.button("Predict"):
            predictions = best_modelmor.predict(df.values.reshape(1, -1))
            targets = ['Phosphorous01', 'Phosphorous02', 'Nitrogen01', 'Nitrogen02', 'Potassium01', 'Potassium02']
            
            for i, target in enumerate(targets):
                df[target] = predictions[0, i]

            df["NPKratio01"] = df.apply(calculate_npk_ratio01, axis=1)
            df["NPKratio02"] = df.apply(calculate_npk_ratio02, axis=1)

            df["Meaning"] = df.apply(lambda row: recommend_action(row["NPKratio01"], row["NPKratio02"]), axis=1)
            
            

            for index, row in df.iterrows():
                st.write(f"#### NPK01 Ratio Value: {row['NPKratio01']}")
                st.write(f"#### NPK02 Ratio Value: {row['NPKratio02']}")
                st.write("#### Recommendation")
                st.write(row['Meaning'])
                st.write("---")
            st.success("Predictions and Recommendation Action added to your data based on manual input!")
            
            plot_npk_ratios(df.copy())
            

    else:
        st.warning("Please select a valid data input method.")

# Run the Streamlit app only when the script is executed directly
if __name__ == '__main__':
    run()
