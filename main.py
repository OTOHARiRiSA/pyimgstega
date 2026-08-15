from PIL import Image
import numpy as np
import os
import time

def gen_outputs_dir():
    try:
        os.makedirs("output", exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory: {e}")
        return
    
def open_img():
    light_img = input("Enter the path to the light/front image: ").strip()
    dark_img = input("Enter the path to the dark/back image: ").strip()
    
    try:
        light_image = Image.open(light_img)
        dark_image = Image.open(dark_img)
    except Exception as e:
        print(f"Error opening images: {e}")
        return None, None
    
    if light_image.size != dark_image.size:
        print("Error: Images must be of the same size.")
        return None, None
    
    return light_image, dark_image

def gen_mirage_img(light_image, dark_image):
    luminance_light_image = light_image.convert('L')
    luminance_dark_image = dark_image.convert('L')
    return luminance_light_image, luminance_dark_image

def mix_images(light_image, dark_image):
    A = np.array(light_image, dtype=np.float32)
    B = np.array(dark_image, dtype=np.float32)
    
    alpha = (B - A + 255) / 2
    intensity = 0.8
    alpha = (alpha - 128) * intensity + 128
    alpha = np.clip(alpha, 0, 255).astype(np.uint8)
    
    R = (A.astype(np.float32) * alpha + B.astype(np.float32) * (255 - alpha)) / 255
    R = np.clip(R, 0, 255).astype(np.uint8)
    output_img = np.zeros((A.shape[0], A.shape[1], 4), dtype=np.uint8)
    output_img[..., 0] = R
    output_img[..., 1] = R
    output_img[..., 2] = R
    output_img[..., 3] = alpha
    
    return output_img


def main():
    
    gen_outputs_dir()
    
    light_image, dark_image = open_img()
    
    if light_image is None or dark_image is None:
        return

    luminance_light_image, luminance_dark_image = gen_mirage_img(light_image, dark_image)
    
    output_img = mix_images(luminance_light_image, luminance_dark_image)
    
    output_img = Image.fromarray(output_img, mode='RGBA')
    
    current_time = time.strftime("%Y%m%d_%H%M%S")
    output_img.save(f"output/output_image_{current_time}.png", "PNG", compress_level=0)
    
    print(f"Mirage image generated successfully! Path: output/output_image_{current_time}.png")
    
if __name__ == "__main__":  
    main()