def documentation_markdown():
    # Read markdown content from a file named "content.txt"
    try:
        with open('content.txt', 'r', encoding='utf-8') as file:
            markdown_text = file.read()
    except FileNotFoundError:
        print("Error: 'content.txt' not found.")

    # Optionally process the markdown_text if needed.
    # For this example, we'll simply output it.
    print(markdown_text)

documentation_markdown()

# ====================================================================================================================

from PIL import Image

def compress_image(input_path, output_path):
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Save the image in WebP format with lossless compression.
        # 'method=6' uses the slowest but most efficient compression.
        img.save(output_path, format='WEBP', lossless=True, method=6)
        print(f"Compressed image saved to {output_path}")
    except Exception as e:
        print("Error compressing image:", e)


input_path = "shapes.png"
output_path = "compressed_shapes.png"
compress_image(input_path, output_path)

# ====================================================================================================================

