import os
import json
import torch
from pathlib import Path
from video_generator import ImageToVideoGenerator, AudioProcessor, FaceExtractor

def load_config(config_path='config.json'):
    """Yapılandırma dosyasını yükle"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_pipeline(config=None):
    """
    Tam işlem hattını çalıştır:
    1. Resimden video oluştur
    2. Videoyu ses uzunluğuna ayarla
    3. Ses ekle
    4. (İsteğe bağlı) Yüz taşı
    """
    
    if config is None:
        config = load_config()
    
    print("\n" + "="*60)
    print("🎬 AI VIDEO GENERATOR - BAŞLANIYOR")
    print("="*60)
    
    # Klasörleri kontrol et
    input_image = config['input']['image_path']
    input_audio = config['input']['audio_path']
    
    if not os.path.exists(input_image):
        print(f"❌ Hata: Resim bulunamadı: {input_image}")
        print(f"   Lütfen resminizi '{input_image}' yoluna koyun")
        return
    
    if not os.path.exists(input_audio):
        print(f"❌ Hata: Müzik bulunamadı: {input_audio}")
        print(f"   Lütfen müziğinizi '{input_audio}' yoluna koyun")
        return
    
    # Çıktı klasörünü oluştur
    os.makedirs('output', exist_ok=True)
    os.makedirs('temp', exist_ok=True)
    
    # ADIM 1: Resimden Video Oluştur
    print("\n📸 ADIM 1: Resimden video oluşturuluyor...")
    print(f"   Resim: {input_image}")
    
    generator = ImageToVideoGenerator()
    
    prompt = config['input']['prompt']
    duration = config['video_settings']['duration_seconds']
    fps = config['video_settings']['fps']
    num_frames = config['video_settings']['num_frames']
    
    try:
        frames = generator.generate_video_from_image(
            image_path=input_image,
            prompt=prompt,
            duration_seconds=duration,
            fps=fps,
            num_frames=num_frames
        )
        
        temp_video = config['output']['video_output']
        generator.save_video(frames, temp_video, fps=fps)
        print(f"   ✅ Video oluşturuldu: {temp_video}")
        
    except Exception as e:
        print(f"❌ Video oluşturmada hata: {str(e)}")
        return
    
    # ADIM 2: Videoyu Ses Uzunluğuna Ayarla
    print("\n🎵 ADIM 2: Video ses uzunluğuna ayarlanıyor...")
    
    try:
        audio_duration = AudioProcessor.get_audio_duration(input_audio)
        print(f"   Ses süresi: {audio_duration:.2f} saniye")
        
        adjusted_video = 'temp/video_adjusted.mp4'
        AudioProcessor.adjust_video_to_audio(temp_video, input_audio, adjusted_video)
        print(f"   ✅ Video ayarlandı")
        
    except Exception as e:
        print(f"❌ Video ayarlamada hata: {str(e)}")
        adjusted_video = temp_video
    
    # ADIM 3: Ses Ekle
    print("\n🔊 ADIM 3: Ses videoya ekleniyor...")
    
    try:
        final_video = config['output']['final_output']
        AudioProcessor.add_audio_to_video(adjusted_video, input_audio, final_video)
        print(f"   ✅ Final video oluşturuldu: {final_video}")
        
    except Exception as e:
        print(f"❌ Ses eklenmesinde hata: {str(e)}")
        return
    
    # ADIM 4: (İsteğe bağlı) Yüz Taşı
    if config['face_swap']['enabled']:
        print("\n😊 ADIM 4: Yüz taşıması yapılıyor...")
        print("   ⚠️  Bunun için Roop yüklü olması gerekir")
        print("   İndir: https://github.com/s0md3v/roop")
        
        try:
            face_image = config['face_swap']['source_face']
            if os.path.exists(face_image):
                print(f"   Yüz resmi: {face_image}")
                # FaceExtractor.swap_faces_in_video(final_video, face_image, final_video)
                print("   💡 Manuel olarak Roop kullanarak yüz taşıyabilirsiniz")
            else:
                print(f"   ❌ Yüz resmi bulunamadı: {face_image}")
        except Exception as e:
            print(f"❌ Yüz taşımasında hata: {str(e)}")
    
    # Başarı Mesajı
    print("\n" + "="*60)
    print("✨ TAMAMLANDI!")
    print("="*60)
    print(f"\n📁 Final video: {final_video}")
    print("\nVideo özelikleri:")
    print(f"  • Prompt: {prompt}")
    print(f"  • Ses süresi: {audio_duration:.2f} saniye")
    print(f"  • FPS: {fps}")
    print(f"  • Çözünürlük: {config['video_settings']['width']}x{config['video_settings']['height']}")
    
    print("\n💡 İPUÇLARİ:")
    print("  • Daha iyi sonuç için prompt'u detaylı yazın")
    print("  • Yüz taşımak için Roop kullanabilirsiniz")
    print("  • Farklı promptlar deneyin (config.json'da)")
    
    return final_video

def run_batch_generation(config=None):
    """Birden fazla prompt ile video oluştur"""
    
    if config is None:
        config = load_config()
    
    print("\n" + "="*60)
    print("🎬 TOPLU VIDEO OLUŞTURMA")
    print("="*60)
    
    generator = ImageToVideoGenerator()
    input_image = config['input']['image_path']
    input_audio = config['input']['audio_path']
    
    prompts = config.get('prompts', [config['input']['prompt']])
    
    for i, prompt in enumerate(prompts):
        print(f"\n\n📹 Video {i+1}/{len(prompts)}: {prompt}")
        
        # Yapılandırmayı güncelle
        config['input']['prompt'] = prompt
        config['output']['video_output'] = f'temp/video_{i}.mp4'
        config['output']['final_output'] = f'output/video_{i}_final.mp4'
        
        # Çalıştır
        run_pipeline(config)

if __name__ == "__main__":
    import sys
    
    print("🎬 AI VIDEO GENERATOR")
    print("\nSeçenekler:")
    print("  1. Tek video oluştur (default)")
    print("  2. Toplu video oluştur")
    print("  3. Yüz taşımasını aç/kapat")
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == 'batch':
            run_batch_generation()
        elif mode == 'swap':
            config = load_config()
            config['face_swap']['enabled'] = True
            run_pipeline(config)
        else:
            run_pipeline()
    else:
        run_pipeline()
