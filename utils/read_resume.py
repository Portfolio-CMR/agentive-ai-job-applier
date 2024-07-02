from docx import Document

def read_word_document(file_path: str) -> str:
    """
    Reads the text from a Word document (.docx) and returns it as a string.

    :param file_path: The path to the Word document file.
    :return: The text content of the document.
    """
    try:
        doc = Document(file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading the Word document: {e}")
        raise