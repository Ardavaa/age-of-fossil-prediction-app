import numpy as np
import pickle as pkl
import streamlit as st
import plotly.express as px

# Load the classifier and scalers
with open('.pkl/regressor.pkl', 'rb') as pickle_in:
    regressor = pkl.load(pickle_in)

def make_prediction(uranium_lead_ratio, carbon_14_ratio, radioactive_decay_series, stratigraphic_layer_depth, geological_period, paleomagnetic_data,
                     inclusion_of_other_fossils, isotopic_composition, surrounding_rock_type, stratigraphic_position, fossil_size, fossil_weight):
    # label mapping
    stratigraphic_position_mapping = {'Middle': 0, 'Top': 1, 'Bottom': 2}
    paleomagnetic_data_mapping = {'Normal polarity': 0, 'Reversed polarity': 1}
    surrounding_rock_type_mapping = {'Sandstone': 0, 'Limestone': 1, 'Shale': 2, 'Conglomerate': 3}
    inclusion_of_other_fossils_mapping = {'Yes': 0, 'No': 1}
    geological_period_mapping = {
        'Triassic': 0,
        'Ordovician': 1,
        'Jurassic': 2,
        'Neogene': 3,
        'Permian': 4,
        'Cambrian': 5,
        'Devonian': 6,
        'Silurian': 7,
        'Cretaceous': 8,
        'Paleogene': 9,
        'Carboniferous': 10
    }

    # convert categorical features to numerical
    stratigraphic_position = stratigraphic_position_mapping[stratigraphic_position]
    paleomagnetic_data = paleomagnetic_data_mapping[paleomagnetic_data]
    surrounding_rock_type = surrounding_rock_type_mapping[surrounding_rock_type]
    inclusion_of_other_fossils = inclusion_of_other_fossils_mapping[inclusion_of_other_fossils]
    geological_period = geological_period_mapping[geological_period]

    input_data = np.array([uranium_lead_ratio, carbon_14_ratio, radioactive_decay_series, stratigraphic_layer_depth, geological_period, paleomagnetic_data,
                            inclusion_of_other_fossils, isotopic_composition, surrounding_rock_type,
                            stratigraphic_position, fossil_size, fossil_weight])

    # Make prediction
    prediction = regressor.predict([input_data])
    return prediction

# main function for our web
def main():
    st.set_page_config(page_title="Age of a Fossil Prediction App", page_icon="🦴", layout="centered")
    st.header("Age of a Fossil Prediction App")
    st.write("Please enter the following information to predict the age of a fossil:")


    with st.form(key='prediction_form'):
        uranium_lead_ratio = st.number_input("What is the Uranium-Lead Ratio (0.0 - 1.32)", value=0.0, min_value=0.0, max_value=1.32)
        carbon_14_ratio = st.number_input("What is the Carbon-14 Ratio (0.0 - 1.0)", value=0.0, min_value=0.0, max_value=1.0)
        radioactive_decay_series = st.number_input("What is the Radioactive Decay Series (0.0 - 1.53)", value=0.0, min_value=0.0, max_value=1.53)
        stratigraphic_layer_depth = st.number_input("What is the Stratigraphic Layer Depth (1.20 - 525.0)", value=1.20, min_value=1.20, max_value=525.0)
        geological_period = st.selectbox("What is the Geological Period of the fossil", ['Triassic', 'Ordovician', 'Jurassic', 'Neogene', 'Permian', 'Cambrian', 'Devonian', 'Silurian', 'Cretaceous', 'Paleogene', 'Carboniferous'])
        paleomagnetic_data = st.selectbox("What is the Paleomagnetic Data of the fossil", ['Normal polarity', 'Reversed polarity'])
        inclusion_of_other_fossils = st.selectbox("Is there any other fossils in the same layer?", ['Yes', 'No'])
        isotopic_composition = st.number_input("What is the Isotopic Composition (0.0 - 3.15)", value=0.0, min_value=0.0, max_value=3.15)
        surrounding_rock_type = st.selectbox("What is the Surrounding Rock Type", ['Sandstone', 'Limestone', 'Shale', 'Conglomerate'])
        stratigraphic_position = st.selectbox("What is the Stratigraphic Position of the fossil", ['Middle', 'Top', 'Bottom'])
        fossil_size = st.number_input("What is the Fossil Size (1.36 - 177.0)", value=1.36, min_value=1.36, max_value=177.0)
        fossil_weight = st.number_input("What is the Fossil Weight (0.05 - 1000.0)", value=0.05, min_value=0.05, max_value=1000.0)

        # predict button
        submit_button = st.form_submit_button(label='Predict')
    
    if submit_button:
        # make prediction
        prediction = make_prediction(uranium_lead_ratio, carbon_14_ratio, radioactive_decay_series, stratigraphic_layer_depth, geological_period, paleomagnetic_data,
                                    inclusion_of_other_fossils, isotopic_composition, surrounding_rock_type, stratigraphic_position, fossil_size, fossil_weight)

        # display the prediction
        st.success(f"The predicted age of the fossil is {int(round(prediction[0]))} years.")

if __name__ == '__main__':
    main()
