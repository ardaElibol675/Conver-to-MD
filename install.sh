#!/usr/bin/env bash
# convert_md kurulum betiği: sanal ortamı oluşturur, bağımlılıkları kurar
# ve ~/.local/bin altına bir convert_md komutu yazar.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
BIN_DIR="$HOME/.local/bin"
TARGET="$BIN_DIR/convert_md"

echo "-> Sanal ortam oluşturuluyor: $VENV_DIR"
python3 -m venv "$VENV_DIR"

echo "-> Bağımlılıklar kuruluyor..."
"$VENV_DIR/bin/pip" install --upgrade pip >/dev/null
"$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

mkdir -p "$BIN_DIR"

echo "-> Komut yazılıyor: $TARGET"
cat > "$TARGET" <<EOF
#!/usr/bin/env bash
exec "$VENV_DIR/bin/python3" "$PROJECT_DIR/script.py" "\$@"
EOF
chmod +x "$TARGET"

echo
echo "[TAMAMLANDI] convert_md kuruldu: $TARGET"
if ! command -v convert_md >/dev/null 2>&1; then
    echo "Uyarı: $BIN_DIR PATH içinde görünmüyor. ~/.bashrc dosyanıza şunu ekleyin:"
    echo '  export PATH="$HOME/.local/bin:$PATH"'
fi
