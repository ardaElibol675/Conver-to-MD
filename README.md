# convert-md

[markitdown](https://github.com/microsoft/markitdown) kütüphanesini kullanarak PDF (ve markitdown'ın desteklediği diğer) dosyaları Markdown formatına dönüştüren komut satırı aracı.

## Kurulum

```bash
git clone git@github.com:ardaElibol675/Conver-to-MD.git
cd Conver-to-MD
./install.sh
```

`install.sh` şunları yapar:
- Proje klasörü içinde bir Python sanal ortamı (`venv/`) oluşturur.
- `requirements.txt` içindeki bağımlılıkları (`markitdown`, `openai`) kurar.
- `~/.local/bin/convert_md` adında, sanal ortamı kullanan bir çalıştırılabilir dosya oluşturur.

`~/.local/bin` klasörünün PATH içinde olduğundan emin olun (çoğu Linux dağıtımında varsayılan olarak eklidir). Değilse `~/.bashrc` dosyanıza şunu ekleyin:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Kurulumdan sonra yeni bir terminal açın veya `source ~/.bashrc` çalıştırın.

## Kullanım

```bash
convert_md dosya.pdf
convert_md dosya.pdf --use-ai
```

- Varsayılan mod: markitdown'ın yerel dönüştürücüsünü kullanır (hızlı, ücretsiz).
- `--use-ai`: OpenAI GPT-4o ile görselleri ve LaTeX formüllerini de işler. Bunun için `OPENAI_API_KEY` ortam değişkeninin ayarlı olması gerekir.

Çıktı, girdi dosyasıyla aynı klasörde, dosya adıyla aynı isimde bir klasör altında oluşturulur:

```
dosya/
├── dosya.md
├── dosya.zip
└── images/   (varsa gömülü görseller)
```
