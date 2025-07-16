from PIL import Image

def detect_image_type(path):
    with Image.open(path) as img:
        return img.format.lower()

if __name__ == "__main__":
    # Point to the file you just added
    print(detect_image_type("test.jpg"))