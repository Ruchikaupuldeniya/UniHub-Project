import os
import google.generativeai as genai

class BotService:
    _api_configured = False

    @classmethod
    def initialize(cls) -> bool:
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                cls._api_configured = True
                return True
            except Exception as e:
                print(f"Error configuring Gemini API: {e}")
                cls._api_configured = False
        return False

    @classmethod
    def get_reply(cls, message: str, is_admin: bool = False) -> str:
        """
        Generates a response using Gemini or mock response based on settings.
        """
        if not cls._api_configured:
            cls.initialize()

        if cls._api_configured:
            try:
                if is_admin:
                    system_prompt = (
                        "You are 'UniHub Admin Assistant', an AI administrative support assistant for administrators at the University of Vavuniya, Sri Lanka. "
                        "Help admins with inquiries about deactivating/activating student portals, checking directory stats, managing faculties, "
                        "and general portal operation guidelines in a professional, helpful tone. "
                        "Keep your responses concise, useful, and formatted in markdown."
                    )
                else:
                    system_prompt = (
                        "You are 'UniHub Companion', an AI academic assistant for students at the University of Vavuniya, Sri Lanka. "
                        "Help students with inquiries about their coursework, departments, campus life, GPA calculations, "
                        "and other administrative topics in a friendly, supportive, and professional tone. "
                        "Keep your responses concise, useful, and formatted in markdown."
                    )
                
                # Create a simple generative model
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"{system_prompt}\n\nUser Message: {message}")
                return response.text
            except Exception as e:
                print(f"Error generating content via Gemini: {e}")
                return cls._get_mock_reply(message, is_admin)
        else:
            return cls._get_mock_reply(message, is_admin)

    @classmethod
    def _get_mock_reply(cls, message: str, is_admin: bool = False) -> str:
        msg = message.lower().strip()
        
        if is_admin:
            if "hello" in msg or "hi" in msg:
                return (
                    "Hello Administrator! I am your **UniHub Admin Assistant**. How can I help you manage the student portal today?"
                )
            elif "deactivate" in msg or "block" in msg or "status" in msg or "suspend" in msg:
                return (
                    "To **deactivate or activate a student portal**:\n\n"
                    "1. Navigate to the **Student Directory** tab in the sidebar.\n"
                    "2. Locate the student using the search bar (search by name or Reg No).\n"
                    "3. Click the toggle switch in the 'Deactivate Toggle' column.\n\n"
                    "Deactivated students will be blocked from logging in immediately and will see an account suspended message."
                )
            elif "stats" in msg or "statistics" in msg or "chart" in msg or "metric" in msg:
                return (
                    "To **view system metrics and charts**:\n\n"
                    "1. Navigate to the **Stats Panel** tab in the sidebar.\n"
                    "2. You can view total registered, active, and deactivated portals.\n"
                    "3. Scroll down to see a visual bar chart of student distribution across different faculties."
                )
            elif "faculty" in msg or "faculties" in msg:
                return (
                    "The University of Vavuniya currently has three active faculties:\n"
                    "- **Faculty of Applied Science** (Pampaimadu)\n"
                    "- **Faculty of Business Studies** (Vavuniya Town / Pampaimadu)\n"
                    "- **Faculty of Technological Studies** (Pampaimadu)"
                )
            else:
                return (
                    "As your **UniHub Admin Assistant**, I can assist you with administrative guides.\n\n"
                    "You can ask me about:\n"
                    "- *How to deactivate/activate students*\n"
                    "- *System statistics and faculty charts*\n"
                    "- *Vavuniya University campus details*"
                )
        else:
            # Simple intelligent response matching about University of Vavuniya
            if "hello" in msg or "hi" in msg:
                return (
                    "Hello! I am your **UniHub Companion**. How can I assist you with your academic journey at the "
                    "University of Vavuniya today?"
                )
            elif "gpa" in msg or "calculate" in msg:
                return (
                    "To calculate your **Grade Point Average (GPA)**:\n\n"
                    "1. Multiply the grade points of each course by its credit value.\n"
                    "2. Sum all the products up.\n"
                    "3. Divide by the total number of credits taken.\n\n"
                    "You can view your current GPA breakdown in the **GPA Tracker** tab of this app!"
                )
            elif "applied science" in msg:
                return (
                    "The **Faculty of Applied Science** includes:\n"
                    "- Department of Physical Science\n"
                    "- Department of Bio-Science\n\n"
                    "It offers undergraduate degrees in Computer Science, Applied Mathematics, Information Technology, and Environmental Science."
                )
            elif "business" in msg or "management" in msg:
                return (
                    "The **Faculty of Business Studies** includes:\n"
                    "- Department of Financial Management\n"
                    "- Department of Management & Entrepreneurship\n"
                    "- Department of English Language Teaching"
                )
            elif "technol" in msg or "ict" in msg:
                return (
                    "The **Faculty of Technological Studies** includes:\n"
                    "- Department of Information & Communication Technology\n"
                    "- Department of Engineering Technology\n\n"
                    "It is located at the Pampaimadu campus."
                )
            elif "location" in msg or "where" in msg:
                return (
                    "The **University of Vavuniya** is situated in Vavuniya, Sri Lanka.\n"
                    "The main administrative building and the Faculty of Applied Science are situated at the Pampaimadu campus, Vavuniya."
                )
            else:
                return (
                    "Thank you for asking! As your **UniHub Companion**, I'm here to help. "
                    "I can guide you about Vavuniya University faculties (Applied Science, Business Studies, Technological Studies), "
                    "GPA calculations, or help you navigate your student portal. "
                    "Could you please specify your question?"
                )
