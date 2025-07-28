import re
def sanitize_text(text):

    # Replace Markdown symbols (** __ # ` ~ > - etc.) with commas
    text = re.sub(r'[*_#`~>\-]+', ':', text)

    # Replace HTML tags like <b>, </div>, etc. with a colon
    text = re.sub(r'<[^>]+>', ':', text)

    # Clean up leading/trailing whitespace and redundant commas
    text = re.sub(r'(^, |, $)', '', text).strip()
    
    return text