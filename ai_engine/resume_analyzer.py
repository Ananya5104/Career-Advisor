import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_resume(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    return {"skills": skills}
