import os
import json

"""
Traveres the directory where the vbs are place.
basedirectory/
└── file draw/
    └── documentname/
        ├── file.pdf
        └── Chromadb/
"""

def list_dir(
    start_directory, ignore_dir="chroma_db"
):
    # Calculate the depth for directories two levels below the start_directory
    direcs = []
    dirlist = {}
    target_depth = len(os.path.abspath(start_directory).split(os.sep)) + 1

    for root, dirs, files in os.walk(start_directory, topdown=True):
        # Calculate the current depth of root
        current_depth = len(os.path.abspath(root).split(os.sep))

        # If we are at the first level, remove the ignore_dir if it exists
        if current_depth == target_depth - 1:
            if ignore_dir in dirs:
                dirs.remove(
                    ignore_dir
                )  # This modifies the list in-place, affecting the walk

        # If we are at the second level, print the directory and its immediate children
       
        if current_depth == target_depth:
            parent_dir = os.path.basename(root)
            for dir_name in dirs:
              if parent_dir not in dirlist:
                   dirlist[parent_dir] = [dir_name]
              else:
                   dirlist[parent_dir].append(dir_name)
              print(f"{parent_dir}/{dir_name}")
              direcs.append(f"{parent_dir}/{dir_name}")
    #print(dirlist)
    json_string = json.dumps(dirlist, indent=4)
    return json_string
