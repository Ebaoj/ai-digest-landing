#!/usr/bin/env python3
"""
Processa o logo do AI Digest para criar todos os assets necessários:
- Favicon (múltiplos tamanhos)
- Ícone do cristal (sem texto)
- Tipografia separada
- Versões com fundo transparente
"""

from PIL import Image
import os

# Diretório de saída
OUTPUT_DIR = "/Users/joabecornelio/ai-digest-landing/assets/brand"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def remove_background(img):
    """Remove o fundo cinza claro da imagem"""
    # Converter para RGBA se necessário
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    data = img.getdata()
    new_data = []

    # O fundo é cinza claro (#E8E8E8 aproximadamente)
    for item in data:
        r, g, b, a = item
        # Se é cinza claro (todos os valores RGB próximos e altos)
        if r > 220 and g > 220 and b > 220 and abs(r-g) < 10 and abs(g-b) < 10:
            new_data.append((255, 255, 255, 0))  # Transparente
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img

def extract_icon(img):
    """Extrai apenas o ícone do cristal (parte superior)"""
    width, height = img.size

    # O ícone está aproximadamente nos 60% superiores
    icon_height = int(height * 0.65)

    # Encontrar os limites do cristal
    # Vamos pegar a região superior
    icon = img.crop((0, 0, width, icon_height))

    # Encontrar bbox do conteúdo não transparente
    bbox = icon.getbbox()
    if bbox:
        icon = icon.crop(bbox)

    return icon

def extract_text(img):
    """Extrai apenas o texto 'AI DIGEST' (parte inferior)"""
    width, height = img.size

    # O texto está aproximadamente nos 35% inferiores
    text_start = int(height * 0.65)

    text = img.crop((0, text_start, width, height))

    # Encontrar bbox do conteúdo
    bbox = text.getbbox()
    if bbox:
        text = text.crop(bbox)

    return text

def create_favicon_sizes(icon_img):
    """Cria favicons em múltiplos tamanhos"""
    sizes = [16, 32, 48, 64, 128, 180, 192, 512]

    for size in sizes:
        # Redimensionar mantendo aspect ratio e centralizando em quadrado
        icon_copy = icon_img.copy()
        icon_copy.thumbnail((size, size), Image.Resampling.LANCZOS)

        # Criar imagem quadrada com padding
        favicon = Image.new('RGBA', (size, size), (0, 0, 0, 0))

        # Centralizar
        x = (size - icon_copy.width) // 2
        y = (size - icon_copy.height) // 2
        favicon.paste(icon_copy, (x, y), icon_copy)

        favicon.save(os.path.join(OUTPUT_DIR, f"favicon-{size}x{size}.png"))
        print(f"  ✅ favicon-{size}x{size}.png")

    # Criar favicon.ico (multi-resolução)
    icon_16 = Image.open(os.path.join(OUTPUT_DIR, "favicon-16x16.png"))
    icon_32 = Image.open(os.path.join(OUTPUT_DIR, "favicon-32x32.png"))
    icon_48 = Image.open(os.path.join(OUTPUT_DIR, "favicon-48x48.png"))

    icon_16.save(
        os.path.join(OUTPUT_DIR, "favicon.ico"),
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print("  ✅ favicon.ico (multi-resolução)")

def main():
    print("=" * 50)
    print("PROCESSAMENTO DO LOGO AI DIGEST")
    print("=" * 50)

    # Carregar imagem original
    input_path = os.path.join(OUTPUT_DIR, "logo_original.png")

    if not os.path.exists(input_path):
        print(f"\n❌ Arquivo não encontrado: {input_path}")
        print("\nPor favor, salve a imagem do logo neste caminho.")
        return

    print(f"\n📂 Carregando: {input_path}")
    img = Image.open(input_path)
    print(f"   Tamanho original: {img.size}")

    # 1. Remover fundo
    print("\n🔲 Removendo fundo...")
    img_transparent = remove_background(img)
    img_transparent.save(os.path.join(OUTPUT_DIR, "logo_transparent.png"))
    print("  ✅ logo_transparent.png")

    # 2. Extrair ícone (cristal)
    print("\n💎 Extraindo ícone do cristal...")
    icon = extract_icon(img_transparent)
    icon.save(os.path.join(OUTPUT_DIR, "icon_crystal.png"))
    print(f"  ✅ icon_crystal.png ({icon.size})")

    # 3. Extrair texto
    print("\n📝 Extraindo tipografia...")
    text = extract_text(img_transparent)
    text.save(os.path.join(OUTPUT_DIR, "typography.png"))
    print(f"  ✅ typography.png ({text.size})")

    # 4. Criar favicons
    print("\n🌐 Criando favicons...")
    create_favicon_sizes(icon)

    # 5. Criar versão para Apple Touch Icon
    print("\n📱 Criando Apple Touch Icon...")
    apple_icon = Image.new('RGBA', (180, 180), (255, 255, 255, 255))
    icon_scaled = icon.copy()
    icon_scaled.thumbnail((140, 140), Image.Resampling.LANCZOS)
    x = (180 - icon_scaled.width) // 2
    y = (180 - icon_scaled.height) // 2
    apple_icon.paste(icon_scaled, (x, y), icon_scaled)
    apple_icon.save(os.path.join(OUTPUT_DIR, "apple-touch-icon.png"))
    print("  ✅ apple-touch-icon.png")

    # 6. Criar OG Image (para redes sociais)
    print("\n🖼️ Criando OG Image (1200x630)...")
    og_img = Image.new('RGBA', (1200, 630), (24, 24, 27, 255))  # Fundo escuro

    # Adicionar logo completo centralizado
    logo_scaled = img_transparent.copy()
    logo_scaled.thumbnail((400, 400), Image.Resampling.LANCZOS)
    x = (1200 - logo_scaled.width) // 2
    y = (630 - logo_scaled.height) // 2
    og_img.paste(logo_scaled, (x, y), logo_scaled)
    og_img.save(os.path.join(OUTPUT_DIR, "og-image.png"))
    print("  ✅ og-image.png")

    # Resumo
    print("\n" + "=" * 50)
    print("✅ PROCESSAMENTO CONCLUÍDO!")
    print("=" * 50)
    print(f"\n📁 Assets salvos em: {OUTPUT_DIR}")
    print("\nArquivos criados:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
        print(f"  • {f} ({size:,} bytes)")

if __name__ == "__main__":
    main()
