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

def mirage_mode(A, B, alpha):
    R = (A.astype(np.float32) * alpha + B.astype(np.float32) * (255 - alpha)) / 255
    R = np.clip(R, 0, 255).astype(np.uint8)
    output_img = np.zeros((A.shape[0], A.shape[1], 4), dtype=np.uint8)
    output_img[..., 0] = R
    output_img[..., 1] = R
    output_img[..., 2] = R
    output_img[..., 3] = alpha
    return output_img

def color_mode(A, B, alpha):
    R = (A[..., 0].astype(np.float32) * alpha + B[..., 0].astype(np.float32) * (255 - alpha)) / 255
    G = (A[..., 1].astype(np.float32) * alpha + B[..., 1].astype(np.float32) * (255 - alpha)) / 255
    B = (A[..., 2].astype(np.float32) * alpha + B[..., 2].astype(np.float32) * (255 - alpha)) / 255
    R = np.clip(R, 0, 255).astype(np.uint8)
    G = np.clip(G, 0, 255).astype(np.uint8)
    B = np.clip(B, 0, 255).astype(np.uint8)
    output_img = np.zeros((A.shape[0], A.shape[1], 4), dtype=np.uint8)
    output_img[..., 0] = R
    output_img[..., 1] = G
    output_img[..., 2] = B
    output_img[..., 3] = alpha
    return output_img

def mix_images(light_image, dark_image, mode='mirage'):
    A = np.array(light_image, dtype=np.float32)
    B = np.array(dark_image, dtype=np.float32)
    
    alpha = (B - A + 255) / 2
    intensity = 0.8
    alpha = (alpha - 128) * intensity + 128
    alpha = np.clip(alpha, 0, 255).astype(np.uint8)
    
    if mode == 'mirage':
        output_img = mirage_mode(A, B, alpha)
    elif mode == 'color':
        output_img = color_mode(A, B, alpha)
    else:
        raise ValueError("Invalid mode. Choose 'mirage' or 'color'.")
    
    return output_img


def main():
    
    gen_outputs_dir()
    
    light_image, dark_image = open_img()
    
    if light_image is None or dark_image is None:
        return
    
    mode = input("Enter mode ('mirage' or 'color'): ").strip().lower()
    if mode not in ['mirage', 'color']:
        print("Invalid mode. Please choose 'mirage' or 'color'.")
        return
    if mode == 'mirage':
        print("Mirage mode selected. The output will be a grayscale image with alpha channel.")
        light_image, dark_image = gen_mirage_img(light_image, dark_image)
    else:
        print("Color mode selected. The output will be a color image with alpha channel.")
    
    
    output_img = mix_images(light_image, dark_image, mode=mode)
    
    output_img = Image.fromarray(output_img, mode='RGBA')
    
    current_time = time.strftime("%Y%m%d_%H%M%S")
    output_img.save(f"output/output_image_{current_time}.png", "PNG", compress_level=0)
    
    print(f"{mode.capitalize()} image generated successfully! Path: output/output_image_{current_time}.png")
    
if __name__ == "__main__":  
    main()