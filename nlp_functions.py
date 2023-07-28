import os
import unittest
from unittest.mock import patch, MagicMock
from transformers import pipeline

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Expected environment variable '{var_name}' not set."
        raise Exception(error_msg)

def summarize_text(text):
    summarizer = pipeline('summarization')
    try:
        summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return None

    return summary[0]['summary_text']

def translate_text(text, target_language):
    translator = pipeline('translation_en_to_' + target_language)
    try:
        translation = translator(text, max_length=40)
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

    return translation[0]['translation_text']

class TestNLPTasks(unittest.TestCase):
    @patch('transformers.pipeline')
    def test_summarize_text(self, mock_pipeline):
        mock_summarizer = MagicMock()
        mock_pipeline.return_value = mock_summarizer
        mock_summarizer.return_value = [{'summary_text': 'Summary'}]
        self.assertEqual(summarize_text('Test text'), 'Summary')

    @patch('transformers.pipeline')
    def test_translate_text(self, mock_pipeline):
        mock_translator = MagicMock()
        mock_pipeline.return_value = mock_translator
        mock_translator.return_value = [{'translation_text': 'Translation'}]
        self.assertEqual(translate_text('Test text', 'fr'), 'Translation')

# Uncomment to run the unit tests
# if __name__ == "__main__":
#     unittest.main()