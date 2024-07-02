from docx import Document

def string_to_word_doc(text, filename):
    # Create a new Document
    doc = Document()
    
    # Add a paragraph with the given text
    doc.add_paragraph(text)
    
    # Save the document
    doc.save(filename)

