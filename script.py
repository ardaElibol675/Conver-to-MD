#!/usr/bin/env python3
import os
import sys
import shutil
from markitdown import MarkItDown
from openai import OpenAI

def print_usage():
    print("Kullanım: convert_md <pdf_dosya_yolu> [--use-ai]")
    print("Örnek:    convert_md ders_notu.pdf")
    print("Örnek AI: convert_md ders_notu.pdf --use-ai")

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    input_path = sys.argv[1]
    use_ai = "--use-ai" in sys.argv

    if not os.path.exists(input_path):
        print(f"Hata: '{input_path}' dosyası bulunamadı!")
        sys.exit(1)

    # Yol ve isim dinamiklerini ayarla
    abs_input_path = os.path.abspath(input_path)
    current_dir = os.path.dirname(abs_input_path)
    base_name = os.path.splitext(os.path.basename(abs_input_path))[0]
    
    # 1. İSTEK: Klasör adı sadece base_name olacak
    target_dir = os.path.join(current_dir, base_name)
    image_dir = os.path.join(target_dir, "images")
    md_output_path = os.path.join(target_dir, f"{base_name}.md")

    # Klasör yönetimini yap (Temiz kurulum)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(image_dir, exist_ok=True)

    print(f"\n[İŞLEM BAŞLADI] Dosya: {os.path.basename(abs_input_path)}")
    print(f"Hedef Klasör: {target_dir}")

    # MarkItDown Kurulumu
    if use_ai:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Hata: --use-ai modu seçildi ancak OPENAI_API_KEY çevre değişkeni bulunamadı!")
            # Temizleme yapıp çıkalım
            shutil.rmtree(target_dir)
            sys.exit(1)
        print("-> OpenAI GPT-4o entegrasyonu aktif (LaTeX formülleri ve grafikler işleniyor)...")
        client = OpenAI(api_key=api_key)
        md = MarkItDown(llm_client=client, llm_model="gpt-4o")
    else:
        print("-> Standart yerel dönüşüm aktif (Hızlı ve ücretsiz)...")
        md = MarkItDown()

    try:
        # Dönüştürme işlemini başlat
        result = md.convert(abs_input_path, image_dir=image_dir)
        
        # Markdown dosyasını kaydet
        with open(md_output_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
            
        print("-> Metin yapısı ve döküman unsurları kaydedildi.")

        # Eğer images klasörü boş kaldıysa temizle (görüntü kirliliği olmasın diye)
        if not os.listdir(image_dir):
            os.rmdir(image_dir)
            print("-> PDF içinde ham gömülü resim bulunamadığı için boş images klasörü temizlendi.")

        # 2. İSTEK: Zip dosyası yeni oluşturulan klasörün İÇİNDE oluşacak
        print("-> Yapay zeka uyumlu ZIP arşivi klasörün içinde hazırlanıyor...")
        
        # Geçici bir isimle zip oluşturup klasör içine taşıyacağız (kendi kendini sıkıştırma hatası vermemesi için)
        temp_zip_base = os.path.join(current_dir, f"temp_{base_name}")
        shutil.make_archive(temp_zip_base, 'zip', target_dir)
        
        # Oluşan geçici zip dosyasını hedef klasörün içine taşı ve adını düzelt
        final_zip_path = os.path.join(target_dir, f"{base_name}.zip")
        shutil.move(f"{temp_zip_base}.zip", final_zip_path)
        
        print(f"\n[BAŞARILI]")
        print(f" Tüm çıktılar bu klasörün altında toplandı: {target_dir}")
        print(f" └── {base_name}.md")
        print(f" └── {base_name}.zip (AI'a yüklemek için hazır)")

    except Exception as e:
        print(f"\n[HATA] Dönüşüm sırasında bir sorun oluştu: {e}")
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        sys.exit(1)

if __name__ == "__main__":
    main()