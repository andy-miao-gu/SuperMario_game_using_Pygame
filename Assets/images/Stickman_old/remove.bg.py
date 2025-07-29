import os
from rembg import remove
from PIL import Image

# Root folder containing all animation folders (current directory)
root_dir = os.path.dirname(os.path.abspath(__file__))

# List of subfolders to process
folders = ["Jump", "standing", "Stickman walk"]

# Output folder to store no-background images
output_root = os.path.join(root_dir, "no_bg")
os.makedirs(output_root, exist_ok=True)

for folder in folders:
    input_path = os.path.join(root_dir, folder)
    output_path = os.path.join(output_root, folder)
    
    # Check if input folder exists
    if not os.path.exists(input_path):
        print(f"❌ Folder not found: {input_path}")
        continue
        
    os.makedirs(output_path, exist_ok=True)
    print(f"📁 Processing folder: {folder}")

    for filename in os.listdir(input_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            input_file = os.path.join(input_path, filename)
            output_file = os.path.join(output_path, filename)

            try:
                with Image.open(input_file) as img:
                    print(f"🔄 Processing: {filename}")
                    img_no_bg = remove(img)
                    # Save as PNG to preserve transparency
                    output_file = os.path.splitext(output_file)[0] + ".png"
                    img_no_bg.save(output_file)
                    print(f"✅ Processed: {output_file}")
            except Exception as e:
                print(f"❌ Error processing {filename}: {str(e)}")

print("🎉 Background removal completed!")
