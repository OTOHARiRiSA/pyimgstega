import time
import os

def gen_outputs_dir():
    try:
        os.makedirs("output", exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory: {e}")
        return
    