import os


def create_directory(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Successfully created directory at: {folder_path}")

def main():
    create_directory()

if __name__ == "__main__":
    main()
