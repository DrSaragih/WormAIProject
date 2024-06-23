import streamlit as st
import pandas as pd
import numpy as np

# Load dataset
file_path = 'Feeding Logs.xlsx'
xls = pd.ExcelFile(file_path)
sep_dec_2023 = pd.read_excel(file_path, sheet_name='Sep to Dec 2023')
jan_jun_2024 = pd.read_excel(file_path, sheet_name='Jan to Jun 2024')

# Combine data from both sheets
df = pd.concat([sep_dec_2023, jan_jun_2024], ignore_index=True)
df.fillna('', inplace=True)
df['pH values of worm feed'] = pd.to_numeric(df['pH values of worm feed'], errors='coerce')

# Function to get composition for a given pH value
def get_composition_for_ph(desired_ph):
    df['pH_diff'] = np.abs(df['pH values of worm feed'] - desired_ph)
    closest_index = df['pH_diff'].idxmin()
    recommended_composition = df.loc[closest_index, ['Tank 1', 'Tank 2', 'Tank 3', 'Tank 4', 'Tank 5']]
    composition_table = pd.DataFrame(recommended_composition).reset_index()
    composition_table.columns = ['Tank', 'Composition']
    return composition_table

# Function to get pH value for a given composition
def get_ph_for_composition(composition):
    df['composition_match'] = df.apply(lambda row: sum([1 for tank in ['Tank 1', 'Tank 2', 'Tank 3', 'Tank 4', 'Tank 5'] if composition in str(row[tank])]), axis=1)
    best_match_index = df['composition_match'].idxmax()
    best_match_ph = df.loc[best_match_index, 'pH values of worm feed']
    
    if 5.5 <= best_match_ph <= 7.5:
        additional_info = "This means that the liquid in the soil contains an equal amount of hydrogen and hydroxide ions. The nutrients in the soil can be absorbed."
    else:
        additional_info = "The nutrients in the soil cannot be absorbed; the structure of the soil changes and maybe life cannot be supported."
    
    return best_match_ph, additional_info

# Predefined Q&A
qa_pairs = {
    "What is vermicomposting?": "Vermicomposting is a method of composting using worms (usually red wigglers or Eisenia fetida) to break down organic materials like kitchen scraps and yard waste into nutrient-rich compost.",
    "How do worms affect pH in compost?": "Worms help maintain a neutral pH in compost by consuming acidic and basic materials, and their digestive process balances the pH level as they break down organic matter.",
    "What is the ideal pH range for vermicomposting?": "The ideal pH range for vermicomposting is slightly acidic to neutral, typically between 6.0 and 7.0. This range supports the activity of composting worms and encourages decomposition of organic matter.",
    "How can farmers monitor pH in their worm compost?": "Farmers can monitor pH using pH testing kits designed for soil or compost. They can take samples from different parts of the compost pile and test them regularly to ensure pH remains within the optimal range.",
    "What materials can be added to adjust pH in worm compost?": "To adjust pH in worm compost, farmers can add materials such as crushed eggshells (for alkaline adjustment) or citrus peels (for acidic adjustment). These materials can be added in moderation to maintain a balanced pH level.",
    "What should farmers avoid adding to worm compost to maintain pH balance?": "Farmers should avoid adding materials that are extremely acidic or alkaline, such as large amounts of citrus fruits or ashes, as these can disrupt the pH balance and affect the worms' health.",
    "How often should worm compost be turned to manage pH?": "Turning the compost pile regularly (every 1-2 weeks) helps distribute materials evenly and aerates the compost, which can help regulate pH levels naturally by preventing pockets of acidity or alkalinity from forming.",
    "Can vermicompost pH affect plant growth?": "Yes, pH levels in vermicompost can impact plant growth. Plants have specific pH preferences, and maintaining an optimal pH range in vermicompost ensures that the nutrients released during decomposition are readily available to plants without causing nutrient imbalances or deficiencies.",
    "How long does it take for worms to create compost?": "Under optimal conditions, worms can turn organic waste into compost in as little as 1-3 months. Regular feeding, proper moisture levels, and maintaining an optimal temperature (around 55-77°F or 13-25°C) accelerate the composting process.",
    "What are the benefits of using worm compost for farming?": "Worm compost enriches soil with essential nutrients, improves soil structure and water retention, enhances microbial activity, suppresses plant diseases, and reduces the need for chemical fertilizers, making it an environmentally friendly and sustainable option for farmers."
}

def run():
    st.title("Monitor Soil Acidity")
    st.markdown("""
    Hi there!! I'm **:blue[🤖 WormAi]**, your friendly worm composting assistant. I can help you monitor your soil acidity (pH) and provide recommendations for the optimal compost composition to keep your worms thriving!
    """)
    with st.sidebar:
        st.title("Monitor Soil Acidity")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome! Please choose a topic:\n1. FAQ\n2. PH/Composition Queries"}]
        st.session_state.topic = "main_menu"
        st.session_state.sub_topic = None

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "dataframe" in message:
                st.dataframe(message["dataframe"])

    # Handle user input
    if prompt := st.chat_input("Enter your choice or query:"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        if st.session_state.topic == "main_menu":
            if prompt.strip().lower() in ["1", "faq"]:
                st.session_state.topic = "faq"
                st.session_state.sub_topic = "faq"
                response = "You have selected the FAQ section. Please enter your question."
            elif prompt.strip().lower() in ["2", "ph", "monitoring", "ph/composition"]:
                st.session_state.topic = "ph_composition"
                st.session_state.sub_topic = "ph_composition"
                response = "You have selected the PH/Composition section. Please enter a pH value or composition."
            else:
                response = "Invalid choice. Please enter 1 for FAQ or 2 for PH/Composition Monitoring."
            st.session_state.messages.append({"role": "assistant", "content": response})

        elif st.session_state.topic == "faq":
            if prompt.strip().lower() == "continue":
                response = "Please enter your question."
            elif prompt.strip().lower() == "return to main menu":
                st.session_state.topic = "main_menu"
                st.session_state.sub_topic = None
                response = "Returning to the main menu. Please choose a topic:\n1. FAQ\n2. PH/Composition Monitoring"
            else:
                if prompt in qa_pairs:
                    response = qa_pairs[prompt]
                    response += "\n\nWould you like to continue with FAQ or return to the main menu? Type 'continue' or 'return to main menu'."
                else:
                    response = "Sorry, I couldn't find the answer to your question. Returning to the main menu."
                    st.session_state.topic = "main_menu"
                    st.session_state.sub_topic = None
                    response += "\n\nPlease choose a topic:\n1. FAQ\n2. PH/Composition Queries"
            st.session_state.messages.append({"role": "assistant", "content": response})

        elif st.session_state.topic == "ph_composition":
            if prompt.strip().lower() == "continue":
                response = "Please enter a pH value or composition."
            elif prompt.strip().lower() == "return to main menu":
                st.session_state.topic = "main_menu"
                st.session_state.sub_topic = None
                response = "Returning to the main menu. Please choose a topic:\n1. FAQ\n2. PH/Composition Queries"
            else:
                try:
                    desired_ph = float(prompt)
                    recommended_composition_table = get_composition_for_ph(desired_ph)
                    response = f"Recommended composition for pH {desired_ph}:"
                    with st.chat_message("assistant"):
                        st.dataframe(recommended_composition_table)
                    st.session_state.messages.append({"role": "assistant", "content": response, "dataframe": recommended_composition_table})
                except ValueError:
                    best_match_ph = get_ph_for_composition(prompt)
                    if best_match_ph:
                        response = f"The best matching pH value for the composition '{prompt}' is {best_match_ph}."
                    else:
                        response = f"Sorry, I couldn't find a matching pH value for the composition '{prompt}'."
                response += "\n\nWould you like to continue with PH/Composition Queries or return to the main menu? Type 'continue' or 'return to main menu'."
                st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)
            if "dataframe" in st.session_state.messages[-1]:
                st.dataframe(st.session_state.messages[-1]["dataframe"])

# Run the Streamlit app only when the script is executed directly
if __name__ == '__main__':
    run()
