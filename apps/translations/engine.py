from googletrans import Translator

translator = Translator()

def translate_text(text, language):

    translation = translator.translate(text, dest=language)

    return translation.text