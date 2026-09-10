from google.colab import output  # Colab için
from deep_translator import GoogleTranslator
import json

class PromptTranslator:
    """Türkçe prompt'u İngilizceye çevir"""
    
    @staticmethod
    def translate_turkish_to_english(text):
        """Google Translate kullanarak çevir"""
        try:
            translator = GoogleTranslator(source_language='tr', target_language='en')
            translated = translator.translate(text)
            return translated
        except Exception as e:
            print(f"⚠️  Çeviri hatası: {str(e)}")
            print(f"Lütfen manuel olarak İngilizceye çevirin")
            return text
    
    @staticmethod
    def update_config_with_turkish_prompt(config_path, turkish_prompt):
        """config.json'ı Türkçe prompt ile güncelle"""
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Türkçeyi İngilizceye çevir
        english_prompt = PromptTranslator.translate_turkish_to_english(turkish_prompt)
        
        print(f"\n📝 Türkçe: {turkish_prompt}")
        print(f"🌐 İngilizce: {english_prompt}\n")
        
        # Config'e ekle
        config['input']['prompt'] = english_prompt
        
        # Kaydet
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ config.json güncellendi!")
        
        return english_prompt


# Örnek Kullanım
if __name__ == "__main__":
    
    # Türkçe prompt örnekleri
    turkish_prompts = [
        "Parkta yürüyen bir kız",
        "Kırmızı elbiseli bir kadın oturma odasında dans ediyor",
        "Güneşin altında gülen bir çocuk",
        "Pencereden dışarı bakan bir adam",
        "Sahilde yürüyüş yapan bir çift"
    ]
    
    print("=" * 60)
    print("TÜRKÇE PROMPT ÇEVİRİCİ")
    print("=" * 60)
    
    for prompt in turkish_prompts:
        translated = PromptTranslator.translate_turkish_to_english(prompt)
        print(f"TR: {prompt}")
        print(f"EN: {translated}\n")
