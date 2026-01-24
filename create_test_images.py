from PIL import Image, ImageDraw
import os

src_dir = r'd:\PlayGround\badge_generator\badge_generator\images\source\src_img'

filenames = [
    'Hồ Đức Hải_T815714_VP_2.bmp',
    'Lâm Sơn Đình Đại_B672542_SD_2.png',
    'Nguyễn Nhật Quốc_455189_SME_1.jpg',
    'Đặng Tú Yến Mai_B845013_E_2.bmp',
    'Đỗ Hữu Huy_T597678_SE_1.bmp'
]

for filename in filenames:
    # Create a simple test image (200x200 with a color)
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    name_part = filename.split('_')[0][:15]
    draw.text((10, 10), name_part, fill='black')
    
    filepath = os.path.join(src_dir, filename)
    img.save(filepath)
    print(f"Created: {filename}")

print("All test images created successfully!")
