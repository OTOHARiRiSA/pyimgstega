import os
import time

import cli
import tank

def gen_outputs_dir():
    try:
        os.makedirs("output", exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory: {e}")
        return
    


def main():
    
    gen_outputs_dir()
    args = cli.get_args()
    
    assert args.light is not None, "Light image path is required"
    assert args.dark is not None, "Dark image path is required"
    
    light_image, dark_image = tank.open_img(light_path=args.light, dark_path=args.dark)
    
    mode = args.mode
    intensity = args.intensity
    
    if mode == 'mirage':
        print("Mirage mode selected. The output will be a grayscale image with alpha channel.")
    else:
        print("Color mode selected. The output will be a color image with alpha channel.")

    output_img = tank.mix_images(light_image, dark_image, intensity, mode=mode)
    
    output_img = tank.Image.fromarray(output_img, mode='RGBA')
    
    current_time = time.strftime("%Y%m%d_%H%M%S")
    output_img.save(f"output/output_image_{current_time}.png", "PNG", compress_level=0)
    
    print(f"{mode.capitalize()} image generated successfully! Path: output/output_image_{current_time}.png")
    
if __name__ == "__main__":  
    main()