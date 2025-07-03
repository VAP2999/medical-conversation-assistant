import re
import json
from datetime import datetime
import random

class ConversationManager:
    def __init__(self):
        self.conversation_history = []
        self.empathy_keywords = [
            'worried', 'scared', 'anxious', 'confused', 'frustrated', 
            'pain', 'hurt', 'afraid', 'concerned', 'stressed'
        ]
        
        self.symptom_keywords = {
            'pain': ['pain', 'ache', 'hurt', 'sore', 'tender'],
            'fatigue': ['tired', 'exhausted', 'fatigue', 'weak', 'energy'],
            'fever': ['fever', 'hot', 'chills', 'temperature'],
            'breathing': ['breath', 'breathing', 'chest', 'cough'],
            'digestive': ['stomach', 'nausea', 'vomit', 'diarrhea', 'appetite']
        }
        
    def generate_response(self, user_input, communication_style, anxiety_level, symptom_data):
        """Generate human-centered AI response"""
        
        # Detect emotional state
        emotional_words = [word for word in self.empathy_keywords if word.lower() in user_input.lower()]
        
        # Adapt to communication style
        if communication_style == "Empathetic & Gentle":
            tone = self._get_empathetic_tone(emotional_words, anxiety_level)
        elif communication_style == "Direct & Factual":
            tone = self._get_direct_tone()
        else:  # Casual & Friendly
            tone = self._get_casual_tone()
        
        # Generate personalized response
        response = self._create_personalized_response(user_input, tone, anxiety_level, emotional_words)
        
        # Add human agency preservation
        response += self._add_agency_preservation()
        
        return response
    
    def _get_empathetic_tone(self, emotional_words, anxiety_level):
        if emotional_words or anxiety_level >= 4:
            return {
                'opening': "I can understand this must be concerning for you. ",
                'validation': "Your feelings about this are completely valid. ",
                'support': "Let's work together to help you organize these thoughts. "
            }
        return {
            'opening': "Thank you for sharing that with me. ",
            'validation': "I'm here to help you prepare for your visit. ",
            'support': "Let's explore this together. "
        }
    
    def _get_direct_tone(self):
        return {
            'opening': "Based on what you've shared, ",
            'validation': "This information will be helpful for your doctor. ",
            'support': "Let me help you organize this clearly. "
        }
    
    def _get_casual_tone(self):
        return {
            'opening': "Thanks for letting me know about that! ",
            'validation': "That's useful information to share with your doctor. ",
            'support': "Let's get this organized for your visit. "
        }
    
    def _create_personalized_response(self, user_input, tone, anxiety_level, emotional_words):
        response = tone['opening']
        
        # Add validation if emotional content detected
        if emotional_words or anxiety_level >= 4:
            response += tone['validation']
        
        # Generate specific follow-up questions
        follow_up = self._generate_follow_up_questions(user_input)
        response += follow_up
        
        # Add support statement
        response += "\n\n" + tone['support']
        
        return response
    
    def _generate_follow_up_questions(self, user_input):
        """Generate contextual follow-up questions"""
        
        # Detect symptom categories
        detected_symptoms = []
        for category, keywords in self.symptom_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                detected_symptoms.append(category)
        
        questions = []
        
        if 'pain' in detected_symptoms:
            questions.extend([
                "Can you describe the pain? Is it sharp, dull, throbbing, or something else?",
                "When did this pain start?",
                "Does anything make it better or worse?"
            ])
        
        if 'fatigue' in detected_symptoms:
            questions.extend([
                "How long have you been feeling this tired?",
                "Is this different from your usual energy levels?",
                "Does rest help, or do you still feel tired after sleeping?"
            ])
        
        if 'fever' in detected_symptoms:
            questions.extend([
                "Have you taken your temperature?",
                "Are you experiencing chills or sweating?",
                "Any other symptoms along with the fever?"
            ])
        
        # If no specific symptoms detected, ask general questions
        if not questions:
            questions = [
                "When did you first notice this?",
                "Has it been getting better, worse, or staying the same?",
                "Is there anything that seems to trigger it or make it better?"
            ]
        
        # Select 1-2 most relevant questions
        selected_questions = random.sample(questions, min(2, len(questions)))
        
        response = "To help you prepare for your doctor visit, I'd like to understand a bit more:\n\n"
        for i, question in enumerate(selected_questions, 1):
            response += f"{i}. {question}\n"
        
        return response
    
    def _add_agency_preservation(self):
        """Add statements that preserve human agency and doctor authority"""
        agency_statements = [
            "\n\n💡 Remember: These questions are just to help you organize your thoughts. Your doctor will ask the important medical questions and provide the expert assessment you need.",
            "\n\n🤝 I'm here to help you communicate clearly with your healthcare provider, who will make the actual medical evaluation.",
            "\n\n👩‍⚕️ Your doctor has the medical expertise to properly evaluate your symptoms and recommend appropriate care."
        ]
        
        return random.choice(agency_statements)
    
    def extract_symptom_info(self, user_input):
        """Extract and structure symptom information"""
        symptom_data = {}
        
        # Extract timeline information
        timeline_patterns = [
            r'(\d+)\s+(day|week|month)s?\s+ago',
            r'for\s+(\d+)\s+(day|week|month)s?',
            r'since\s+(yesterday|last\s+\w+)',
            r'started\s+(yesterday|today|last\s+\w+)'
        ]
        
        for pattern in timeline_patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                symptom_data['timeline'] = match.group(0)
                break
        
        # Extract severity indicators
        severity_words = {
            'mild': ['little', 'slight', 'mild', 'minor'],
            'moderate': ['moderate', 'noticeable', 'uncomfortable'],
            'severe': ['severe', 'intense', 'unbearable', 'extreme', 'terrible', 'awful']
        }
        
        for level, words in severity_words.items():
            if any(word in user_input.lower() for word in words):
                symptom_data['severity'] = level
                break
        
        # Extract location information
        body_parts = [
            'head', 'neck', 'chest', 'back', 'stomach', 'abdomen', 
            'arm', 'leg', 'hand', 'foot', 'knee', 'shoulder'
        ]
        
        for part in body_parts:
            if part in user_input.lower():
                symptom_data['location'] = part
                break
        
        # Store the original input with timestamp
        symptom_data['reported_at'] = datetime.now().isoformat()
        symptom_data['description'] = user_input
        
        return symptom_data