import streamlit as st
import pandas as pd
from datetime import datetime
import json
from conversation_manager import ConversationManager
from utils import generate_doctor_summary, detect_urgency_level

# Page configuration
st.set_page_config(
    page_title="Medical Conversation Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'conversation_manager' not in st.session_state:
    st.session_state.conversation_manager = ConversationManager()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'symptom_data' not in st.session_state:
    st.session_state.symptom_data = {}

def main():
    st.title("🏥 Medical Conversation Assistant")
    st.markdown("### Helping you prepare for your healthcare visit")
    
    # Important disclaimer
    st.warning("""
    ⚠️ **Important**: This is a preparation tool only. I cannot diagnose medical conditions. 
    Always consult with qualified healthcare professionals for medical advice.
    """)
    
    # Sidebar for personalization
    with st.sidebar:
        st.header("🎯 Personalization Settings")
        
        communication_style = st.selectbox(
            "How would you like me to communicate?",
            ["Empathetic & Gentle", "Direct & Factual", "Casual & Friendly"]
        )
        
        anxiety_level = st.slider(
            "How anxious are you feeling about your symptoms? (1=calm, 5=very anxious)",
            1, 5, 3
        )
        
        visit_type = st.selectbox(
            "What type of healthcare visit are you preparing for?",
            ["General Check-up", "Specific Symptom Discussion", "Follow-up Visit", "Specialist Consultation"]
        )
        
        st.markdown("---")
        st.markdown("### 🤝 Human-AI Collaboration")
        st.info("I'm here to help you organize your thoughts, not replace your doctor's expertise.")
    
    # Main conversation area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Conversation")
        
        # Display conversation history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Tell me about what's concerning you..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            response = st.session_state.conversation_manager.generate_response(
                prompt, 
                communication_style, 
                anxiety_level,
                st.session_state.symptom_data
            )
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
            
            # Update symptom data
            st.session_state.symptom_data = st.session_state.conversation_manager.extract_symptom_info(prompt)
    
    with col2:
        st.subheader("📋 Your Visit Preparation")
        
        if st.session_state.symptom_data:
            st.markdown("**Symptoms Discussed:**")
            for symptom, details in st.session_state.symptom_data.items():
                st.write(f"• {symptom}: {details}")
        
        if len(st.session_state.messages) > 2:
            if st.button("📄 Generate Doctor Summary"):
                summary = generate_doctor_summary(st.session_state.messages, st.session_state.symptom_data)
                st.markdown("### Summary for Your Doctor")
                st.text_area("Share this with your healthcare provider:", summary, height=200)
                
                # Urgency assessment
                urgency = detect_urgency_level(st.session_state.symptom_data)
                if urgency == "high":
                    st.error("⚠️ Based on what you've shared, you should seek medical attention promptly.")
                elif urgency == "medium":
                    st.warning("⏰ Consider scheduling an appointment within the next few days.")
                else:
                    st.success("💚 This seems appropriate for a routine medical consultation.")
        
        # Questions for doctor
        st.markdown("### 🤔 Questions to Ask Your Doctor")
        suggested_questions = [
            "What could be causing these symptoms?",
            "Are there any tests you'd recommend?",
            "What can I do to manage this at home?",
            "When should I follow up with you?",
            "Are there warning signs I should watch for?"
        ]
        
        for i, question in enumerate(suggested_questions):
            if st.checkbox(f"{question}", key=f"q_{i}"):
                st.session_state.symptom_data[f"question_{i}"] = question
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>🤝 This tool enhances human healthcare relationships - it doesn't replace them.</p>
    <p>Built with human-centered AI principles for better doctor-patient communication.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()