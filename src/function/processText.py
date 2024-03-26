import re

# Remove redundant tag of the text
def processText_removeTag(text):
    # Remove unnecessary tags
    text = re.sub(r'<[^>]+>', '', text)
    text = ' '.join(text.split())
    # Replace newline characters with periods to split into sentences
    text = text.replace('\\n', '\n\n')
    text = text.replace('\n', '\n\n')
    text = text.replace('%%', '<int> ')
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Remove empty sentences, strip extra spacing, and remove trailing period
    sentences = [sentence.strip().rstrip(' ')
                    for sentence in sentences if sentence.strip()]
    # Return processed sentences
    return sentences


def processText_removeFirstTag(text):
    clean = re.compile(r'^.*?>', re.MULTILINE)
    text = re.sub(clean, '', text)
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Remove empty sentences, strip extra spacing, and remove trailing period
    sentences = [sentence.strip().rstrip(' ')
                    for sentence in sentences if sentence.strip()]
    return sentences


# Remove white space
def processText_removeSpace(text):
    # Split into sentences
    output = re.sub(r'\n+', '\n', text)
    return output