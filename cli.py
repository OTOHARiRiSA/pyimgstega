import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Get the paths to the light and dark images, intensity, and mode.")
    parser.add_argument("--light", "-l", type=str, help="Path to the light/front image.", required=True)
    parser.add_argument("--dark", "-d", type=str, help="Path to the dark/back image.", required=True)
    parser.add_argument("--intensity", "-i", type=float, default=0.8, help="Intensity of the mix (default: 0.8).")
    parser.add_argument("--mode", "-m", type=str, choices=['mirage', 'color'], default='mirage', help="Mode of mixing: 'mirage' or 'color' (default: 'mirage').")
    return parser.parse_args()

