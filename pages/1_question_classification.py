import streamlit as st
import requests

# from api_util.question_classification_api import create_QuestionCategory
import api_util.question_classification_api as q_api

# st.balloons()
with st.sidebar:
    st.title("Navigation")
    # page = st.radio("Go to", ["Main Page", "Question classification", "Retrievel"])

# Application title
st.title("Question Classifier")

employee_id = st.text_input("Input your employee ID", value="")

# Model selection dropdown
model = st.selectbox("Select Model", ["gpt-3.5-turbo CHAT", "gpt-4.0", "gpt-3.0"])

# Initialize category count and input boxes
if 'category_count' not in st.session_state:
    st.session_state['category_count'] = 2

# Render input boxes based on current category count
for i in range(1, st.session_state['category_count'] + 1):
    st.markdown(f"#### Category {i}")
    st.text_input(f"LLM classification description {i}", key=f"category_{i}")

# Add category button
if st.button("Add Category", key='add_button_below'):
    st.session_state['category_count'] += 1
    st.rerun()

# Explanation text
st.markdown("Define the classification conditions of user questions, LLM can define how the conversation progresses based on the classification description.")

# Deploy settings button
if st.button("Deploy settings"):
    data = {}
    for i in range(1, st.session_state['category_count'] + 1):
        data[f"category_{i}"] = st.session_state.get(f"category_{i}", "")

    # st.write(data) # for test
    # response = call_api(data)
    # st.write(response)

    if all(value for value in data.values()) and (employee_id != ""):
        st.balloons()
        st.success("Settings deployed successfully!")
        discription_list = [value for value in data.values()]

        request_body = {}
        request_body['employeeId'] = employee_id
        request_body['model'] = model
        request_body['description'] = discription_list
        st.write(request_body)

        
        get_response = q_api.get_QuestionCategory(employee_id)
        if get_response:
            # print(get_response)
            response = q_api.update_QuestionCategory(employee_id, request_body)
            st.write(f"Update response by {employee_id}")
            st.write(response)
        else:
            response = q_api.create_QuestionCategory(request_body)
            st.write(f"Create response by {employee_id}")
            st.write(response)
 
        # for post_item in discription_list:
        #     request_body = {}
        #     request_body['description'] = post_item
        #     print(request_body)

        #     response = create_QuestionCategory(request_body)
        #     st.write(response)
    else:
        st.error("Please fill in all the fields.")