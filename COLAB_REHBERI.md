# 📖 Google Colab Kullanım Rehberi

## 🚀 Başlamadan Önce

1. **Google Hesabı Aç** → https://colab.research.google.com
2. **Notebook Aç**: Yukarıda bulunan `AI_Video_Generator_Colab.ipynb` dosyasını indir ve Colab'a yükle

---

## 📋 Adım Adım Kurulum (5 dakika)

### 1️⃣ Runtime Türünü Değiştir (ÇOK ÖNEMLİ!)

```
Menu → Runtime → Change runtime type
Seç: GPU (T4 veya P100)
```

**Neden?** Video oluşturma GPU gerektirir. CPU ile 10+ saat sürer.

---

### 2️⃣ Hücreler Sırasıyla Çalıştır

Notebook'ta hücreler var:
1. ✅ GPU Kontrol
2. ✅ Kütüphaneleri Kur (5-10 dakika)
3. ✅ PyTorch Kur
4. ✅ Kod Tanımlaması
5. ✅ Resim Yükle
6. ✅ Müzik Yükle
7. ✅ Prompt Gir
8. ✅ Video Oluştur (20-30 dakika)
9. ✅ Ses Ekle
10. ✅ Video İndir

**Kurallar:**
- Hücreler yukarıdan aşağıya çalıştırılmalı
- Bir hücre bitene kadar beklemelisiniz
- Tüm hücrelerin altında çıktı olmalı

---

## 📸 Adım 5: Resim Yükleme

Hücre çalıştırılırsa:
```
📸 Lütfen resminizi seçin...
```

**Klasöre tıklayın** → **Dosya Seç** → Resim yükle

✅ Desteklenen Format: JPG, PNG
✅ Boyut: 576x576 ideal (otomatik ayarlanır)

---

## 🎵 Adım 6: Müzik Yükleme

Resim yükledikten sonra müzik yüklenir:

```
🎵 Lütfen müziğinizi seçin...
```

✅ Desteklenen Format: MP3, WAV, M4A
✅ Uzunluk: 6 dakika (360 saniye) optimal

Ses süresi otomatik gösterilir:
```
🔊 Ses süresi: 45.32 saniye
```

---

## 📝 Adım 7: Prompt Girme (Türkçe Desteği)

```
📝 Videonun açıklamasını girin (Türkçe veya İngilizce):
> 
```

**Türkçe Örnekler:**
- "Parkta yürüyen bir kız"
- "Dansçı kırmızı elbisede dans ediyor"
- "Güneş batarken pencere kenarında oturoyan birisi"

**İngilizce Örnekler:**
- "a girl walking in the park"
- "a dancer in a red dress dancing"
- "person standing by the window at sunset"

✅ Türkçe otomatik İngilizceye çevrilir
✅ Detaylı yazarsanız daha iyi sonuç alırsınız

---

## 🎬 Adım 8: Video Oluştur (EN UZUN ADIM)

```
============================================================
🎬 VIDEO OLUŞTURMA BAŞLIYOR
============================================================
⏱️  Bu işlem 20-30 dakika alabilir, lütfen bekleyin...
```

**Bu sırada:**
- Hücre çıktısını izleyin
- Bilgisayarı uyku moduna almayın
- İnternet bağlantısı kesmeyin

**İlerleme göstergesi:**
```
0%|          | 0/24 [00:00<?, ?it/s]
```

Sabrıyla bekleyin! ⏳

---

## 🔊 Adım 9: Ses Ekle

Video oluşturulduktan sonra otomatik ses eklenir:

```
============================================================
🔊 SES EKLENİYOR
============================================================
```

Bu hızlı bitir (1-2 dakika).

---

## 🎥 Adım 10: Video İndir

Son hücre videonuzu indirir:

```
💾 Video indirilmeye hazırlanıyor...
✅ İndirme başladı!
   Video tarayıcının İndirilenler klasörüne kaydedildi.
```

**Video Konumu:**
- Windows/Mac/Linux: İndirilenler klasörü
- Dosya adı: `final_video.mp4`

---

## ⚠️ Sık Sorunlar & Çözümleri

### ❌ "GPU not found"
```
RuntimeError: CUDA is not available
```
**Çözüm:**
1. Runtime → Change runtime type
2. GPU seçin (T4)
3. Hücreyi tekrar çalıştır

---

### ❌ "CUDA out of memory"
```
RuntimeError: CUDA out of memory
```
**Çözüm:**
- Runtime → Restart runtime
- Baştan başla
- Veya Notebook'a prompt ekleyin:
```python
import torch
torch.cuda.empty_cache()
```

---

### ❌ "Model yüklenmedi"
```
ConnectionError: Failed to download model
```
**Çözüm:**
- İnternet bağlantısı kontrol edin
- İlk download 5-10 dakika sürebilir
- Sabırlı bekleyin

---

### ❌ "Hücre yanıt vermiyor"
```
Connection lost / Timeout
```
**Çözüm:**
- Runtime → Restart runtime
- Baştan başla (kütüphaneleri tekrar kur)
- Veya yeni hücre oluştur

---

### ❌ "Resim/Müzik bulunamadı"
```
FileNotFoundError: No such file
```
**Çözüm:**
- Resim ve Müzik hücrelerini tekrar çalıştır
- Dosyaları tekrar yükle

---

### ❌ "FFmpeg hatası"
```
FileNotFoundError: ffmpeg not found
```
**Çözüm:**
- Bu hata Colab'ta normalde olmaz
- Runtime'ı yenile

---

## 💡 İpuçları & Trikler

### Hızlı Test
- Önce küçük bir müzik yükleyin (30 saniye)
- Basit bir prompt deneyin
- Tam ürün için uzun müzik yükleyin

### Kaliteli Video
- Prompt'u detaylı yazın
- Aydınlatmayı (sunny, dark, etc.) belirtin
- Saç, gözler, kıyafet tanımını ekleyin

### Türkçe Prompt Örnekleri
```
✅ "Uzun siyah saçlı, mavi gözlü kız, parkta yürüyüş yapıyor, güneşli hava"
✅ "Kırmızı elbiseli kadın, oturma odasında dans ediyor, altın ışıklandırma"
✅ "Genç erkek, pencereden dışarı bakıyor, akşam güneşi, melankolik"
```

### Colab Süresini Uzatma
- Her 12 saatte session sona erer
- Kütüphaneleri tekrar kurmanız gerekir
- Videolar kaydedilirse kalır

---

## 📊 Beklenen Süreler

| Adım | Süre | Neler Oluyor |
|------|------|---|
| GPU Kontrol | < 1 dakika | Sistem hazırlanıyor |
| Kütüphaneleri Kur | 5-10 dakika | İlk kez daha uzun alabilir |
| Resim Yükle | < 1 dakika | Dosya yükleniyor |
| Müzik Yükle | < 1 dakika | Dosya yükleniyor |
| Prompt Gir | < 1 dakika | Türkçe çeviri yapılıyor |
| **Video Oluştur** | **20-30 dakika** | 🤖 AI çalışıyor ⏳ |
| Ses Ekle | 1-2 dakika | FFmpeg işleniyor |
| **TOPLAM** | **~30-45 dakika** | ✅ Video hazır |

---

## 🎓 Eğitim: Prompt Yazma Teknikleri

### Temel Yapı
```
[Kişi Tanımı] + [Aktivite] + [Ortam] + [Işık/Atmosfer]
```

### Kişi Tanımı
- "a young woman with long brown hair"
- "a girl in a red dress"
- "a person with blonde hair and blue eyes"

### Aktivite
- "walking in the park"
- "dancing" 
- "sitting by the window"
- "smiling"

### Ortam
- "in a modern living room"
- "in a garden"
- "at a cafe"
- "in a ballroom"

### Işık/Atmosfer
- "with golden lighting"
- "under sunset"
- "with natural sunlight"
- "with dramatic shadows"

### Tam Örnek
```
"A young woman with long dark hair in a blue dress, 
dancing gracefully in a luxurious ballroom with crystal 
chandeliers and golden lighting"
```

---

## 🔐 Güvenlik & Gizlilik

✅ Colab'a yükledikleri dosyalar:
- Sadece sizin Session'unuzda kalır
- 12 saat sonra silinir
- Google tarafından depolanmaz

✅ Oluşturduğunuz videolar:
- Tamamen sizin kontrolünde
- İndirebilir/silebilirsiniz
- Hiç paylaşılmaz

---

## 🔗 Faydalı Linkler

- **Zeroscope**: https://github.com/cerspense/zeroscope_v2
- **Google Colab**: https://colab.research.google.com
- **Hugging Face**: https://huggingface.co
- **Deep Translator**: https://github.com/nidhaloff/deep-translator

---

## ✅ Başlamadan Önce Kontrol Listesi

- [ ] Google Hesabı açılı mı?
- [ ] Colab.research.google.com'a erişebiliyor musunuz?
- [ ] Yüklemek istediğiniz resim var mı? (JPG/PNG)
- [ ] Müzik dosyanız var mı? (MP3/WAV)
- [ ] Prompt'u düşündünüz mü?
- [ ] İnternet bağlantısı stabil mi?
- [ ] Bilgisayar pil modunda değil mi?

---

## 🎬 Tam İş Akışı

```
1. Colab aç → colab.research.google.com
2. Notebook yükle → AI_Video_Generator_Colab.ipynb
3. Runtime değiştir → GPU (T4)
4. Hücreleri çalıştır → Sırasıyla yukarıdan aşağıya
5. Resim yükle → Input olarak
6. Müzik yükle → Input olarak
7. Prompt gir → Türkçe yazabilir
8. Video oluştur → 20-30 dakika bekle
9. Ses ekle → Otomatik
10. İndir → İndirilenler klasörüne
11. Paylaş → Sosyal medyada gösterin! 🎥
```

---

## 🆘 Yardım Alamazsanız

1. **Repository Issues**: https://github.com/erorhan3503-sudo/ai-video-generator/issues
2. **Colab Resmi Yardım**: https://colab.research.google.com/notebooks/welcome.ipynb
3. **Zeroscope Dokümanları**: https://huggingface.co/cerspense/zeroscope_v2_576w

---

## 🎉 Tebrikler!

Artık resimlerden gerçekçi videolar oluşturabiliriz!

**Sonraki Adımlar:**
- Kendi resimlerinizi deneyin
- Farklı promptlar yazın
- Arkadaşlarınıza gösterin

---

**Keyifli video oluşturmalar! 🎥✨**

*Sorularınız varsa GitHub Issues'a yazabilirsiniz.*
