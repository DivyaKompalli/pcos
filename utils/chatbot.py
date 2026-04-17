import streamlit as st
import google.generativeai as genai

def render_chatbot():
    st.subheader("🤖 Health Educator Assistant")
    st.write("Ask dynamic questions about PCOS, Anemia, diet, and lifestyle!")
    
    st.info("Note: This chatbot provides educational information powered by Google's Gemini AI, not medical diagnosis.")
    
    # 1. Fetch API Key securely
    api_key = ""
    if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"] != "paste_your_api_key_here":
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        api_key = st.text_input("Enter your free Gemini API Key (or save it in .streamlit/secrets.toml)", type="password")
    
    if not api_key:
        st.warning("Please enter your Gemini API key above to start the dynamic chat.")
        return
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Error configuring API: {e}")
        return

    # 2. Initialize chat history
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
        try:
            st.session_state.chat_session.send_message(
                "You are a helpful, empathetic, and knowledgeable health educator focusing on Indian women's health, specifically PCOS and Anemia. "
                "You must clarify that you are an AI prototype and NEVER provide clinical diagnoses. "
                "Give practical, evidence-based lifestyle and dietary advice. Keep answers under 3 paragraphs."
            )
            st.session_state.messages = []
        except Exception as e:
            if "not found" in str(e).lower() or "404" in str(e):
                av_models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        av_models.append(m.name)
                st.error(f"Your API key doesn't have access to the default model. Available models for your key: {', '.join(av_models)}")
                return
            else:
                st.error(f"Initialization error: {e}")
                return
        
    # 3. Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # 4. Handle new question
    if prompt := st.chat_input("Ask a health question (e.g., 'What kind of diet helps with PCOS?')..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chat_session.send_message(prompt)
                    bot_reply = response.text
                except Exception as e:
                    bot_reply = f"Sorry, I encountered an error with the API: {e}. Is the API key correct?"
                st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
