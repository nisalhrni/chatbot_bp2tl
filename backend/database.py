from supabase import create_client, Client
import config

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def save_chat_history(session_id: str, user_message: str, bot_response: str):
    try:
        supabase.table("chat_history").insert({
            "session_id": session_id,
            "user_message": user_message,
            "bot_response": bot_response
        }).execute()
    except Exception as e:
        print(f"Error saving chat history: {e}")

def get_all_faq():
    try:
        response = supabase.table("faq").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching FAQ: {e}")
        return []

def get_all_knowledge():
    try:
        response = supabase.table("knowledge").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching knowledge: {e}")
        return []
