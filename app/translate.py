import requests
from flask_babel import _
from app import app

def translate(text, source_language, dest_language):
    if 'OPENROUTER_API_KEY' not in app.config or \
            not app.config['OPENROUTER_API_KEY']:
        return _('Error: the translation service is not configured.')
    
    # Map language codes to full names for better translation quality
    language_names = {
        'en': 'English',
        'zh': 'Chinese',
        'fr': 'French',
        'es': 'Spanish',
        'de': 'German',
        'ja': 'Japanese',
        'ko': 'Korean',
        'ru': 'Russian',
        'pt': 'Portuguese',
        'it': 'Italian',
    }
    
    source_lang_name = language_names.get(source_language, source_language)
    dest_lang_name = language_names.get(dest_language, dest_language)
    
    headers = {
        'Authorization': f"Bearer {app.config['OPENROUTER_API_KEY']}",
        'Content-Type': 'application/json',
        'HTTP-Referer': app.config.get('OPENROUTER_HTTP_REFERER', ''),
        'X-Title': app.config.get('OPENROUTER_APP_NAME', 'Microblog'),
    }
    
    # Create translation prompt
    prompt = f"Translate the following text from {source_lang_name} to {dest_lang_name}. Only return the translated text, without any additional explanation or commentary:\n\n{text}"
    
    payload = {
        'model': 'minimax/minimax-m2',
        'messages': [
            {
                'role': 'system',
                'content': 'You are a professional translator. Translate the given text accurately while preserving the original meaning, tone, and style.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0.3,  # Lower temperature for more consistent translations
    }
    
    try:
        r = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if r.status_code != 200:
            return _('Error: the translation service failed.')
        
        response_data = r.json()
        if 'choices' in response_data and len(response_data['choices']) > 0:
            translated_text = response_data['choices'][0]['message']['content'].strip()
            return translated_text
        else:
            return _('Error: the translation service failed.')
    except Exception as e:
        app.logger.error(f'Translation error: {str(e)}')
        return _('Error: the translation service failed.')
