from fuzzywuzzy import fuzz

def extract_info_fuzzy(text, threshold=80):
    results = {}
    lines = text.split('\n')
    keywords = ["Full role", "Company name"]

    for keyword in keywords:
        for i, line in enumerate(lines):
            if fuzz.partial_ratio(keyword.lower(), line.lower()) >= threshold:
                # Found a match, extract the content
                content = line.split(':', 1)[-1].strip()
                
                # If the content is empty, check the next line
                if not content and i + 1 < len(lines):
                    content = lines[i + 1].strip()
                
                results[keyword] = content
                break
        else:
            # If no match found for this keyword
            results[keyword] = ""
    
    return results

