import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Parser for image mixing options.")
    subparsers = parser.add_subparsers(dest="patterns",required=True, help="Subparser for different patterns.")
    
    # Subparser for 'alpha' pattern
    alpha_parser = subparsers.add_parser("alpha", help="Alpha pattern mixing.")
    alpha_parser.add_argument("--light", "-l", type=str, help="Path to the light/front image.", required=True)
    alpha_parser.add_argument("--dark", "-d", type=str, help="Path to the dark/back image.", required=True)
    alpha_parser.add_argument("--mode", "-m", type=str, choices=["mirage", "color"], default="mirage", help="Mixing mode: 'mirage' for grayscale with alpha channel, 'color' for color with alpha channel (default: mirage).")
    alpha_parser.add_argument("--intensity", "-i", type=float, default=0.8, help="Intensity of the mix (default: 0.8).")
    # Subparser for 'prism' pattern
    prism_parser = subparsers.add_parser("prism", help="Prism pattern mixing.")
    prism_parser.add_argument("--light", "-l", type=str, help="Path to the light/front image.", required=True)
    prism_parser.add_argument("--dark", "-d", type=str, help="Path to the dark/back image.", required=True)
    prism_parser.add_argument("--mode", "-m", type=str, choices=["prism"], default="prism", help="Mixing mode: 'prism' for prism pattern (default: prism).")
    prism_parser.add_argument("--intensity", "-i", type=float, default=0.25, help="Intensity of the mix (default: 0.25).")
    
    return parser.parse_args()

