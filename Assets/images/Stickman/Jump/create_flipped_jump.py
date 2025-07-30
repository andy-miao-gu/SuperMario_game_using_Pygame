import os
from PIL import Image

# Current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Process Jump 1 and Jump 2 images
for i in range(1, 3):  # Jump 1 and Jump 2
    input_file = os.path.join(current_dir, f"Jump {i}.png")
    output_file = os.path.join(current_dir, f"Jump {i}_flipped.png")
    
    try:
        with Image.open(input_file) as img:
            # Flip around x-axis (vertical flip)
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            flipped_img.save(output_file)
            print(f"✅ Created flipped version: Jump {i}_flipped.png")
    except Exception as e:
        print(f"❌ Error processing Jump {i}.png: {str(e)}")

print("🎉 Flipped jump images created!")
