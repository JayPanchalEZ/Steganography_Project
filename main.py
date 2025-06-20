import cv2 as cv
from utils import browse_image, choose_save_path
from stegano_core import encrypt_messg, decrypt_messg, embed_data, extract_data

def main():
    print(" ------- Steganography Tool ------- ")

    while True:
        print("\nChoose an option:")
        print("1. Hide message in Image")
        print("2. Extract message from Image")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            print("Please select the cover image from the pop-up window...")
            input_path = browse_image()
            if not input_path:
                print("Error: No image selected.")
                continue

            image = cv.imread(input_path)
            if image is None:
                print("Error: Could not read input image.")
                continue

            secret = input("Enter the secret message: ")
            key = input("Enter the key: ")

            encrypted = encrypt_messg(secret, key)

            max_bytes = image.shape[0] * image.shape[1] * image.shape[2] // 8 - 4
            if len(encrypted) > max_bytes:
                print("Error: Message too large for this image.")
                continue

            result = embed_data(image, encrypted)

            print("Image is ready to save. Please select where to save it from the pop-up window...")
            output_path = choose_save_path()
            if output_path:
                cv.imwrite(output_path, result)
                print(f"Message embedded and saved to: {output_path}")
            else:
                print("Warning: Save cancelled. Image not saved.")

        elif choice == '2':
            print("Please select the image with hidden message")
            input_path = browse_image()
            if not input_path:
                print("Error: No image selected.")
                continue

            image = cv.imread(input_path)
            if image is None:
                print("Error: Could not read image.")
                continue

            key = input("Enter the key: ")

            try:
                encrypted = extract_data(image)
                message = decrypt_messg(encrypted, key)
                print(f"Hidden or Secret message: {message}")
            except Exception as e:
                print(f"Error: Decryption failed: {e}")

        elif choice == '3':
            print("Thanks for using my Steganography Tool!")
            break

        else:
            print("Error: Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
