from PIL import Image
import numpy as np

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

def prism_mode(A, B, intensity=0.25):
    H, W, _ = A.shape
    
    B = B * intensity
    
    output = np.zeros_like(A)
    x = np.arange(W)
    y = np.arange(H)
    xx, yy = np.meshgrid(x, y)
    mask = (xx + yy) % 2 == 0
    
    output[mask] = A[mask]
    output[~mask] = B[~mask]
    
    return np.clip(output, 0, 255).astype(np.uint8)

#core algorithm
def mix_images(light_image, dark_image, intensity, pattern='alpha', mode='mirage'):
    
    A = np.array(light_image.convert('L'), dtype=np.float32)
    B = np.array(dark_image.convert('L'), dtype=np.float32)
    
    if mode == 'mirage':
        alpha = (B - A + 255) / 2
        alpha = (alpha - 128) * intensity + 128
        alpha = np.clip(alpha, 0, 255).astype(np.uint8)
        output_img = mirage_mode(A, B, alpha)
    elif mode == 'color':
        alpha = (B - A + 255) / 2
        alpha = (alpha - 128) * intensity + 128
        alpha = np.clip(alpha, 0, 255).astype(np.uint8)
        A = np.array(light_image.convert('RGB'), dtype=np.float32)
        B = np.array(dark_image.convert('RGB'), dtype=np.float32)
        output_img = color_mode(A, B, alpha)
    elif mode == 'prism':
        A = np.array(light_image.convert('RGB'), dtype=np.float32)
        B = np.array(dark_image.convert('RGB'), dtype=np.float32)
        output_img = prism_mode(A, B, intensity)
    else:
        raise ValueError("Invalid mode. Choose 'mirage' or 'color'.")
    
    return output_img

def save_img(output_img, mode):
    if mode == 'prism':
        output_img = Image.fromarray(output_img, mode='RGB')
    else:
        output_img = Image.fromarray(output_img, mode='RGBA')
    return output_img