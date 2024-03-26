from PIL import Image

def change_occupancy(input_image_path, opacity):
    # Open the image
    image = Image.open(input_image_path)

    # Convert the image to RGBA mode with an alpha channel
    image = image.convert('RGBA')

    # Adjust the opacity
    data = image.getdata()
    new_data = []
    for item in data:
        r, g, b, a = item
        new_data.append((r, g, b, int(a * opacity)))

    # Update the image with the modified data
    image.putdata(new_data)
    
    # Save the modified image
    return image