from PIL import Image
import numpy as np
import argparse
import os
import time

def get_args():
    parser = argparse.ArgumentParser(description="Get the paths to the light and dark images, intensity, and mode.")
    parser.add_argument("--light", "-l", type=str, help="Path to the light/front image.", required=True)
    parser.add_argument("--dark", "-d", type=str, help="Path to the dark/back image.", required=True)
    parser.add_argument("--intensity", "-i", type=float, default=0.8, help="Intensity of the mix (default: 0.8).")
    parser.add_argument("--mode", "-m", type=str, choices=['mirage', 'color'], default='mirage', help="Mode of mixing: 'mirage' or 'color' (default: 'mirage').")
    return parser.parse_args()

def gen_outputs_dir():
    try:
        os.makedirs("output", exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory: {e}")
        return
    
def open_img(light_path=None, dark_path=None):
    
    try:
        light_image = Image.open(light_path) # type: ignore[arg-type]
        dark_image = Image.open(dark_path) # type: ignore[arg-type]
    except Exception as e:
        print(f"Error opening images: {e}")
        return None, None
    
    if light_image.size != dark_image.size:
        print("Error: Images must be of the same size.")
        return None, None
    
    return light_image, dark_image

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

def mix_images(light_image, dark_image, intensity, mode='mirage'):
    
    A = np.array(light_image.convert('L'), dtype=np.float32)
    B = np.array(dark_image.convert('L'), dtype=np.float32)
    
    alpha = (B - A + 255) / 2
    alpha = (alpha - 128) * intensity + 128
    alpha = np.clip(alpha, 0, 255).astype(np.uint8)
    
    if mode == 'mirage':
        output_img = mirage_mode(A, B, alpha)
    elif mode == 'color':
        A = np.array(light_image.convert('RGB'), dtype=np.float32)
        B = np.array(dark_image.convert('RGB'), dtype=np.float32)
        output_img = color_mode(A, B, alpha)
    else:
        raise ValueError("Invalid mode. Choose 'mirage' or 'color'.")
    
    return output_img


def main():
    
    gen_outputs_dir()
    args = get_args()
    
    assert args.light is not None, "Light image path is required"
    assert args.dark is not None, "Dark image path is required"
    
    light_image, dark_image = open_img(light_path=args.light, dark_path=args.dark)
    
    mode = args.mode
    intensity = args.intensity
    
    if mode == 'mirage':
        print("Mirage mode selected. The output will be a grayscale image with alpha channel.")
    else:
        print("Color mode selected. The output will be a color image with alpha channel.")

    output_img = mix_images(light_image, dark_image, intensity, mode=mode)
    
    output_img = Image.fromarray(output_img, mode='RGBA')
    
    current_time = time.strftime("%Y%m%d_%H%M%S")
    output_img.save(f"output/output_image_{current_time}.png", "PNG", compress_level=0)
    
    print(f"{mode.capitalize()} image generated successfully! Path: output/output_image_{current_time}.png")
    
if __name__ == "__main__":  
    main()