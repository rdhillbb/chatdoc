import os

def list_directories_two_levels_deep_with_condition(start_directory, ignore_dir='chroma_db'):
    # Calculate the depth for directories two levels below the start_directory
    direcs = []
    target_depth = len(os.path.abspath(start_directory).split(os.sep)) + 1

    for root, dirs, files in os.walk(start_directory, topdown=True):
        # Calculate the current depth of root
        current_depth = len(os.path.abspath(root).split(os.sep))

        # If we are at the first level, remove the ignore_dir if it exists
        if current_depth == target_depth - 1:
            if ignore_dir in dirs:
                dirs.remove(ignore_dir)  # This modifies the list in-place, affecting the walk

        # If we are at the second level, print the directory and its immediate children
        if current_depth == target_depth:
            parent_dir = os.path.basename(root)
            for dir_name in dirs:
                print(f"{parent_dir}/{dir_name}")
                direcs.append(f"{parent_dir}/{dir_name}")
    return direcs
# Get the starting directory from the "GOVBOTIC_INGESTION_STORAGE" environment variable
start_directory = os.environ.get("GOVBOTIC_INGESTION_STORAGE")

if start_directory:
    print(f"Listing directories two levels deep from: {start_directory}, ignoring 'chroma_db' at the first level.")
    list_directories_two_levels_deep_with_condition(start_directory)
else:
    print("Environment variable 'GOVBOTIC_INGESTION_STORAGE' is not set.")

