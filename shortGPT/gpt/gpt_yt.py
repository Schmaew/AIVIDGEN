import re

def generate_title_description_dict(content):
    """Generate title and description from content without calling AI API."""
    # Extract first sentence or first 60 chars for title
    content_clean = content.strip()
    
    # Get first line/sentence as title basis
    first_line = content_clean.split('\n')[0].strip()
    first_sentence = re.split(r'[.!?]', first_line)[0].strip()
    
    # Create title (max 60 chars)
    if len(first_sentence) > 60:
        title = first_sentence[:57] + "..."
    elif len(first_sentence) < 10:
        title = first_line[:60] if len(first_line) <= 60 else first_line[:57] + "..."
    else:
        title = first_sentence
    
    # Clean title
    title = re.sub(r'[^\w\s\-\'\"]', '', title).strip()
    if not title:
        title = "Amazing Facts You Need to Know"
    
    # Create description from content excerpt
    desc_text = content_clean[:200].replace('\n', ' ')
    description = f"{desc_text}... #shorts #facts #viral #fyp"
    
    return title, description
