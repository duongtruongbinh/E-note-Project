import os

CHUNK_SIZE = 1024 * 10  # 10KB


def split_file(source_file_name):
    # Check if file_name is file or not
    if os.path.isfile(source_file_name):
        # Get file name and extension
        with open(source_file_name, 'rb') as source_file:
            _, file_extension = os.path.splitext(source_file_name)
            file_size = os.path.getsize(source_file_name)
            os.chdir(os.getcwd() + "\Temp")  # Go to temp directory
            # +1 for the last chunk, if the file is divisible by CHUNK_SIZE, the last chunk will be empty
            
            total_chunk = file_size // CHUNK_SIZE + 1
            for i in range(total_chunk):
                # Chk stand for "chunk"
                with open(str(i) + file_extension + '.chk', 'wb') as f:
                    f.write(source_file.read(CHUNK_SIZE))
                    f.close()
            source_file.close()
            os.chdir("..")
        print("File split successfully")
    else:
        print("File not found")


def merge_file(source_file_name):
    # Check if file_name is file or not
    if os.path.isfile(source_file_name):
        # Get file name and extension
        with open("new" + source_file_name, 'wb') as destination_file:
            _, file_extension = os.path.splitext(source_file_name)
            os.chdir(os.getcwd() + "\Temp")  # Go to temp directory
            
            for i in range(count_file()):
                with open(str(i) + file_extension + '.chk', 'rb') as f:
                    destination_file.write(f.read())
                    f.close()
            destination_file.close()

            # Delete all the .chk files
            for i in range(count_file()):
                os.remove(str(i) + file_extension + '.chk')

            os.chdir("..")
        print("File merge successfully")
    else:
        print("File not found")


def count_file():
    # List all the file with ".chk" suffix in the folder
    os.chdir(f"{os.getcwd()}/Temp")
    file_list = [f for f in os.listdir() if f.endswith('.chk')]  
    # Generator of a list of .chk files
    # Get the most number of ".chk" file
    number_of_files = len(file_list)
    os.chdir("..")
    return number_of_files



