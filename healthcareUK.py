import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st

# Load the pre-trained conversational model from Hugging Face
model_name = "OpenAssistant/oasst-sft-1-pythia-12b"  # You can also use other conversational models
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to generate chatbot responses
def generate_response(user_input, chat_history_ids=None):
    # Encode the user input and append to the chat history (if any)
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    
    # Append new user input to chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids
    
    # Generate a response from the model
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    
    # Decode the response from tokens to string
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    return bot_response, chat_history_ids

# Streamlit UI for chatbot interaction
def main():
    st.title("UK Healthcare Chatbot")
    st.write("Welcome! Ask me anything about healthcare in the UK.")
    
    # Initialize session state for chat history
    if 'chat_history_ids' not in st.session_state:
        st.session_state.chat_history_ids = None
    if 'past_inputs' not in st.session_state:
        st.session_state.past_inputs = []  # To store previous inputs
    if 'past_responses' not in st.session_state:
        st.session_state.past_responses = []  # To store previous bot responses

    # User input from the Streamlit text box
    user_input = st.text_input("You:", "")
    
    if user_input:
        # Generate bot response based on user input
        bot_response, st.session_state.chat_history_ids = generate_response(user_input, st.session_state.chat_history_ids)
        
        # Store the conversation history
        st.session_state.past_inputs.append(user_input)
        st.session_state.past_responses.append(bot_response)
        
        # Display conversation history
        for i in range(len(st.session_state.past_inputs)):
            st.write(f"You: {st.session_state.past_inputs[i]}")
            st.write(f"Bot: {st.session_state.past_responses[i]}")

# Run the chatbot interface
if __name__ == '__main__':
    main()
