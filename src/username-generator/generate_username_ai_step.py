"""
Python Step: Generates Instagram usernames using Gemini AI
Subscribes to 'username.requested' and emits 'username.generated'
"""
import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

config = {
    "type": "event",
    "name": "GenerateUsernamesWithAI",
    "description": "Uses Gemini AI to generate creative Instagram usernames",
    "subscribes": ["username.requested"],
    "emits": ["username.generated"],
    "flows": ["username-generator"],
}


async def handler(input_data, context):
    """
    Handler that uses Gemini API to generate Instagram usernames
    """
    theme = input_data.get("theme", "general")
    keywords = input_data.get("keywords", [])
    count = input_data.get("count", 5)
    request_id = input_data.get("requestId", "unknown")
    
    context.logger.info(f"Generating {count} usernames for theme: {theme}")
    
    # Configure Gemini API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        context.logger.error("GEMINI_API_KEY not found in environment")
        await context.emit({
            "topic": "username.generated",
            "data": {
                "requestId": request_id,
                "success": False,
                "error": "GEMINI_API_KEY not configured",
                "usernames": [],
            }
        })
        return
    
    # Create the prompt for Gemini
    keywords_str = ", ".join(keywords) if keywords else "none specified"
    prompt = f"""Generate exactly {count} unique, creative Instagram usernames based on:

Theme: {theme}
Keywords to incorporate: {keywords_str}

Requirements:
- Each username must be 4-30 characters
- Only use letters, numbers, underscores, and periods
- Make them catchy, memorable, and relevant to the theme
- Ensure they sound like real Instagram usernames people would want
- Mix creative wordplay, abbreviations, and stylistic elements
- Avoid offensive or inappropriate content

Return ONLY the usernames, one per line, no numbering or extra text."""

    try:
        # Use new Google GenAI SDK
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Parse the response
        usernames = [
            line.strip() 
            for line in response.text.strip().split("\n") 
            if line.strip() and len(line.strip()) <= 30
        ][:count]
        
        context.logger.info(f"Generated {len(usernames)} usernames: {usernames}")
        
        # Emit the generated usernames
        await context.emit({
            "topic": "username.generated",
            "data": {
                "requestId": request_id,
                "success": True,
                "theme": theme,
                "keywords": keywords,
                "usernames": usernames,
            }
        })
        
    except Exception as e:
        context.logger.error(f"Error generating usernames: {str(e)}")
        await context.emit({
            "topic": "username.generated",
            "data": {
                "requestId": request_id,
                "success": False,
                "error": str(e),
                "usernames": [],
            }
        })
