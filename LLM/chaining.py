from single_shot import get_cloud_completion
from single_shot import get_oss_completion


def identify_intent(email_text):

    """Step 1: Analyzes the email to determine the category."""
    
    prompt = f"""
    Analyze the following email and categorize it into exactly one of these classes:
    [REFUND, COMPLAINT, PRODUCT_INQUIRY, OTHER]
    
    Return ONLY the category name.
    
    Email: "{email_text}"
    """
    
   
    category = get_cloud_completion(prompt)
    return category.text

def draft_response(email_text, intent):
    
    """Step 2: Drafts a reply based on the identified intent."""
    
    prompt = f"""
    You are a customer support agent.
    Incoming Email: "{email_text}"
    Detected Intent: {intent}
    
    Task: Write a polite, 2-sentence response addressing this specific intent.
    """
    
   
    response = get_oss_completion(prompt)
    return response

def process_email_chain(email_text):
    """The Orchestrator Function linking Step 1 and Step 2."""
    
    
    intent = identify_intent(email_text)
    print(f"DEBUG: Detected Intent -> {intent}")
    
    
    final_response = draft_response(email_text, intent)
    return final_response.choices[0].message.content

customer_email = "I ordered the headset last week and it still hasn't arrived. I want my money back."
print("\nFinal Output:")
print(process_email_chain(customer_email))