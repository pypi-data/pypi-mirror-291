#!/usr/bin/env python3
import argparse
import json
from pylibdmtx.pylibdmtx import encode
from PIL import Image, ImageDraw, ImageFont

def vin_check_digit(vin, board):
    '''
     The check digit, found in position 9 of the VIN, is used to validate the VIN and is compulsory for vehicles 
     in North America. This digit is helpful for computers to immediately tell if there is an error or issue with 
     the VIN. The check digit is calculated by removing all of the letters and substituting them with their 
     appropriate number counterparts. You then take those numbers and multiply them against a weight factor table. 
     You then have 16 numbers which you add together and divide by 11. The remainder is the check digit. If the 
     remainder is 10, then the check digit is X.
    '''
    
    # VIN weight factors according to positions 1-17
    weight_factors = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # VIN transliteration table
    transliteration = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'J': 1, 'K': 2, 'L': 3, 'M': 4,
        'N': 5, 'P': 7, 'R': 9, 'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9,
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }

    # Calculate the sum of the products of the transliterated values and weight factors
    total_sum = 0
    for i in range(17):
        if i == 8:  # Skip the check digit itself
            continue
        total_sum += transliteration[vin[i]] * weight_factors[i]

    # Calculate the remainder when the sum is divided by 11
    remainder = total_sum % 11

    # Determine the check digit
    check_digit = 'X' if remainder == 10 else str(remainder)

    # Verify the check digit
    if vin[8] == check_digit:
        print(f"The VIN for {board} is correct: {vin}")
        return vin
    else:
        corrected_vin = vin[:8] + check_digit + vin[9:]
        print(f"The VIN for {board} is incorrect. Spoofing it with {corrected_vin}.")
        return corrected_vin

def generate_vin_qr(vin):
    # Generate Data Matrix code
    encoded = encode(vin.encode('utf-8'))
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    return img

def add_labels_and_resize(image, board_name, vin, target_height_inch):
    # Define a very large DPI for rendering
    large_dpi = 600  # Large DPI for high-resolution text rendering
    target_height_px = int(target_height_inch * large_dpi)

    # Load a higher-quality font
    font_path = "/Library/Fonts/Arial.ttf"  # Path to a font file on macOS
    font_size = 50  # Larger font size for better rendering initially
    font = ImageFont.truetype(font_path, font_size)

    # Create a larger image with plenty of space for the labels
    large_image = Image.new('RGB', (image.width * 5, image.height * 5 + 140), 'white')
    draw = ImageDraw.Draw(large_image)

    # Draw the board name at the top using textbbox for accurate dimensions
    board_bbox = draw.textbbox((0, 0), board_name, font=font)
    board_label_width = board_bbox[2] - board_bbox[0]
    board_label_height = board_bbox[3] - board_bbox[1] + 10
    board_label_x = (large_image.width - board_label_width) // 2
    draw.text((board_label_x, 0), board_name, fill='black', font=font)

    # Paste the Data Matrix code in the middle
    large_image.paste(image.resize((image.width * 5, image.height * 5), Image.Resampling.NEAREST), (0, board_label_height))

    # Draw the VIN at the bottom using textbbox for accurate dimensions
    vin_bbox = draw.textbbox((0, 0), vin, font=font)
    vin_label_width = vin_bbox[2] - vin_bbox[0]
    vin_label_height = vin_bbox[3] - vin_bbox[1]
    vin_label_x = (large_image.width - vin_label_width) // 2
    draw.text((vin_label_x, board_label_height + image.height * 5), vin, fill='black', font=font)

    # Resize the image down to the target height
    scaling_factor = target_height_px / large_image.height
    target_width_px = int(large_image.width * scaling_factor)
    resized_image = large_image.resize((target_width_px, target_height_px), Image.Resampling.LANCZOS)

    return resized_image

def save_image_as_png(image, file_name):
    # Save the image as PNG
    image.save(file_name, 'PNG')

def main():
    parser = argparse.ArgumentParser(description='Generate QR codes from a JSON file or a given VIN.')
    parser.add_argument('--file', metavar='file', type=str, help='the JSON file to read from')
    parser.add_argument('--vin', metavar='vin', type=str, help='a VIN to generate a QR code for')
    parser.add_argument('--board', metavar='board', type=str, help='a board from the JSON file to generate a QR code for')
    parser.add_argument('--generate-all', action='store_true', help='generate QR codes for all entries in the JSON file')
    args = parser.parse_args()

    # Print help if no arguments are provided
    if not any(vars(args).values()):
        parser.print_help()
        exit(0)

    target_height_inch = 2  # Set the target height to 1.75 inches

    if args.file:
        with open(args.file) as f:
            data = json.load(f)

        if args.generate_all:
            for board in data.keys():
                vin = data[board]['vin']
                final_img = generate_vin_qr(vin_check_digit(vin, board))
                final_img_with_labels = add_labels_and_resize(final_img, board, vin, target_height_inch)
                save_image_as_png(final_img_with_labels, f"{board}.png")
        elif args.board:
            vin = data[args.board]['vin']
            final_img = generate_vin_qr(vin_check_digit(vin, args.board))
            final_img_with_labels = add_labels_and_resize(final_img, args.board, vin, target_height_inch)
            save_image_as_png(final_img_with_labels, f"{args.board}.png")
    elif args.vin:
        final_img = generate_vin_qr(vin_check_digit(args.vin, args.board))
        final_img_with_labels = add_labels_and_resize(final_img, args.vin, args.vin, target_height_inch)
        save_image_as_png(final_img_with_labels, f"{args.vin}.png")
