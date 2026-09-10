import torch
import cv2
import numpy as np
from PIL import Image
import librosa
import soundfile as sf
from pathlib import Path
import os
from diffusers import DiffusionPipeline, DDIMScheduler
import imageio
from scipy.interpolate import interp1d
import warnings
warnings.filterwarnings('ignore')

class ImageToVideoGenerator:
    """Resimden video oluşturucu"""
    
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.device = device
        print(f"Device: {self.device}")
        self.pipe = None
        
    def load_model(self):
        """Zeroscope modelini yükle"""
        print("Model yükleniyor...")
        
        scheduler = DDIMScheduler.from_pretrained(
            "cerspense/zeroscope_v2_576w",
            subfolder="scheduler"
        )
        
        self.pipe = DiffusionPipeline.from_pretrained(
            "cerspense/zeroscope_v2_576w",
            scheduler=scheduler,
            torch_dtype=torch.float16 if self.device == 'cuda' else torch.float32
        )
        self.pipe = self.pipe.to(self.device)
        self.pipe.enable_attention_slicing()
        
        print("Model yüklendi!")
        
    def generate_video_from_image(self, image_path, prompt, duration_seconds=6, fps=24, num_frames=24):
        """
        Resimden video oluştur
        
        Args:
            image_path: Resim dosyasının yolu
            prompt: Video açıklaması (örn: "a person walking in the park")
            duration_seconds: Video uzunluğu (saniye)
            fps: Frame per second
            num_frames: Kaç frame oluşturulacak
        """
        
        if self.pipe is None:
            self.load_model()
        
        # Resmi yükle ve işle
        image = Image.open(image_path).convert("RGB")
        image = image.resize((576, 576))
        
        print(f"Video oluşturuluyor: {prompt}")
        print(f"Süre: {duration_seconds}s, FPS: {fps}, Frames: {num_frames}")
        
        # Video oluştur
        with torch.no_grad():
            video_frames = self.pipe(
                prompt=prompt,
                image=image,
                num_inference_steps=50,
                height=576,
                width=576,
                num_frames=num_frames,
                guidance_scale=7.5
            ).frames
        
        return video_frames
    
    def save_video(self, frames, output_path, fps=24):
        """Video dosyasını kaydet"""
        print(f"Video kaydediliyor: {output_path}")
        
        writer = imageio.get_writer(output_path, fps=fps)
        for frame in frames:
            frame_array = np.array(frame)
            writer.append_data(frame_array)
        writer.close()
        
        print(f"Video kaydedildi!")


class AudioProcessor:
    """Ses işleme"""
    
    @staticmethod
    def get_audio_duration(audio_path):
        """Ses dosyasının uzunluğunu al"""
        y, sr = librosa.load(audio_path)
        duration = librosa.get_duration(y=y, sr=sr)
        return duration
    
    @staticmethod
    def adjust_video_to_audio(video_path, audio_path, output_path):
        """Videoyu ses uzunluğuna göre ayarla"""
        import subprocess
        
        audio_duration = AudioProcessor.get_audio_duration(audio_path)
        
        print(f"Ses uzunluğu: {audio_duration:.2f} saniye")
        print(f"Video ses ile senkronize ediliyor...")
        
        # FFmpeg ile video hızını ayarla
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-filter:v', f'setpts={audio_duration}/N/FRAME_RATE/TB',
            '-y',
            output_path
        ]
        
        subprocess.run(cmd, capture_output=True)
        print("Video ayarlandı!")
    
    @staticmethod
    def add_audio_to_video(video_path, audio_path, output_path):
        """Videoya ses ekle"""
        import subprocess
        
        print(f"Ses videoya ekleniyor...")
        
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-shortest',
            '-y',
            output_path
        ]
        
        subprocess.run(cmd, capture_output=True)
        print("Ses eklendi!")


class FaceExtractor:
    """Yüz çıkarma ve taşıma"""
    
    @staticmethod
    def extract_faces(image_path, output_dir='faces'):
        """Resimden yüzleri çıkar"""
        import subprocess
        
        os.makedirs(output_dir, exist_ok=True)
        
        print("Yüzler çıkarılıyor...")
        
        # MTCNN kullanarak yüz tespiti
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        face_paths = []
        for i, (x, y, w, h) in enumerate(faces):
            face = image[y:y+h, x:x+w]
            face_path = os.path.join(output_dir, f'face_{i}.jpg')
            cv2.imwrite(face_path, face)
            face_paths.append(face_path)
        
        print(f"{len(face_paths)} yüz bulundu!")
        return face_paths
    
    @staticmethod
    def swap_faces_in_video(video_path, face_image_path, output_path):
        """Video içinde yüz değiştir (Roop kullanarak)"""
        print("Yüz taşıması yapılıyor...")
        print("Not: Bu işlem için Roop kurulu olması gerekir")
        print("Roop: https://github.com/s0md3v/roop")


def main():
    print("=" * 50)
    print("AI Video Generator - Resimden Video Oluştur")
    print("=" * 50)
    
    # Klasörleri oluştur
    os.makedirs('input', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    os.makedirs('temp', exist_ok=True)
    
    print("\n1. Resminizi 'input' klasörüne koyun")
    print("2. Müziğinizi 'input' klasörüne koyun")
    print("3. config.json dosyasını düzenleyin")
    print("4. python main.py çalıştırın")
    
    print("\nKullanım örneği:")
    print("  generator = ImageToVideoGenerator()")
    print("  frames = generator.generate_video_from_image(")
    print("      'input/resim.jpg',")
    print("      'a person walking',")
    print("      duration_seconds=6")
    print("  )")


if __name__ == "__main__":
    main()
