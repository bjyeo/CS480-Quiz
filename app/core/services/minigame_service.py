import json
import random
import logging
from openai import OpenAI
from app.config import settings
from fastapi import HTTPException
from app.core.services.supabase import supabase_client

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def get_random_minigame_email():
    try:
        # Get total count of emails
        count_response = supabase_client.from_("minigame_emails").select("*", count="exact").execute()
        total_emails = count_response.count

        if total_emails == 0:
            raise HTTPException(status_code=404, detail="No emails found in database")

        # Get a random offset
        random_offset = random.randint(0, total_emails - 1)
        
        # Fetch one random email
        response = supabase_client.from_("minigame_emails")\
            .select("*")\
            .limit(1)\
            .offset(random_offset)\
            .execute()

        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="No email found")

        # Get the email entry and format it
        email_entry = response.data[0]
        logger.info(f"Retrieved email ID: {email_entry.get('id')}")
        
        # Format email data consistently
        email_data = {
            "from": email_entry.get("from"),
            "to": email_entry.get("to"),
            "subject": email_entry.get("subject"),
            "content": email_entry.get("content")
        }
        
        # 50/50 chance to modify the email
        should_modify = random.choice([True, False])
        
        if should_modify:
            try:
                with open('prompt.txt', 'r') as f:
                    prompt_data = f.read()
                
                # Convert email data to the format specified in the prompt
                email_json = json.dumps(email_data, indent=6)
                
                # Create the full prompt
                full_prompt = f"{prompt_data}\n\nConsidering the previous instructions, rewrite the following email:\n\n{email_json}"
                
                logger.info("Calling OpenAI API with modified prompt")
                
                try:
                    # Make the API call to OpenAI
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": full_prompt,
                            }
                        ],
                        model="gpt-4o-mini",
                    )
                    
                    # Log the raw response for debugging
                    response_text = chat_completion.choices[0].message.content.strip()
                    logger.debug(f"Raw OpenAI response: {response_text}")
                    
                    try:
                        # Look for JSON content
                        start_idx = response_text.find('{')
                        end_idx = response_text.rfind('}') + 1
                        
                        if start_idx >= 0 and end_idx > start_idx:
                            json_str = response_text[start_idx:end_idx]
                            modified_email = json.loads(json_str)
                            logger.info("Successfully parsed OpenAI response as JSON")
                        else:
                            raise ValueError("No JSON object found in response")
                            
                    except (json.JSONDecodeError, ValueError) as e:
                        logger.error(f"JSON parsing error: {str(e)}")
                        logger.error(f"Failed response text: {response_text}")
                        # Create structured response from raw text
                        modified_email = {
                            "from": email_data["from"],
                            "to": email_data["to"],
                            "subject": email_data["subject"],
                            "content": response_text
                        }
                        logger.info("Created structured response from raw text")
                    
                    return {
                        "email": modified_email,
                        "is_modified": True,
                        "prompt_used": full_prompt
                    }
                    
                except Exception as e:
                    logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
                    # Return original email if OpenAI call fails
                    return {
                        "email": email_data,
                        "is_modified": False,
                        "prompt_used": None
                    }
                
            except FileNotFoundError:
                logger.error("Prompt template file not found")
                raise HTTPException(status_code=500, detail="Prompt template file not found")
            except json.JSONDecodeError:
                logger.error("Invalid prompt template file")
                raise HTTPException(status_code=500, detail="Invalid prompt template file")
        
        logger.info(f"Returning unmodified email. ID: {email_entry.get('id')}")
        
        return {
            "email": email_data,
            "is_modified": False,
            "prompt_used": None
        }
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))