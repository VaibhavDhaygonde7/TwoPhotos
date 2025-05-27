from flask import Flask, request, render_template, send_file
import os 
import zipfile
from io import BytesIO
from PIL import Image 

app = Flask(__name__)

UPLOAD_FOLDER = "uploaded_folder"
DOWNLOAD_FOLDER = "downloaded_folder"
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True) 




def resize(background, overlay): 
    bg_width, bg_height = background.size 
    new_overlay_width = int(bg_width * 0.20)
    new_overlay_height = int(bg_height * 0.2) 

    resized_overlay = overlay.resize((new_overlay_width, new_overlay_height))

    return resized_overlay

def addSign(background, overlay, ind):
    background.paste(resize(background, overlay), (900, 1130), resize(background, overlay))

    # Show the image
    # background.show()

    name = ".\downloaded_folder\output" + str(ind) + ".png"

    background.save(name) 

def iterate(folder_path, overlay): 
    ind = 0
    for fileName in os.listdir(folder_path): 
        background = Image.open(folder_path + fileName)
        addSign(background, overlay, ind)
        ind = ind + 1



def delete_files_in_directory(directory_path):
    """
    Deletes all files in the specified directory, but leaves subdirectories intact.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist or is not a directory.")
        return

    print(f"Attempting to delete files in: {directory_path}")
    
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")
        else:
            print(f"Skipping directory/symlink: {file_path}")




@app.route("/upload-folder", methods=["POST"])
def upload_folder(): 
    files = request.files.getlist("images") 
    
    for file in files: 
        fileName = file.filename.replace("/", "_")
        filePath = os.path.join(UPLOAD_FOLDER, fileName)
        file.save(filePath)

    return render_template("download.html")

@app.route("/download-files") 
def download_files(): 
    folder_path = "./uploaded_folder/"
    overlay = Image.open("Signature.png")

    iterate(folder_path, overlay)


    # Create a BytesIO object to store the zip file in memory
    memory_file = BytesIO()

    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(DOWNLOAD_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                # arcname is the path inside the zip file
                # os.path.relpath ensures that the path inside the zip
                # is relative to the DOWNLOAD_FOLDER, not the absolute path
                zf.write(file_path, arcname=os.path.relpath(file_path, DOWNLOAD_FOLDER))

    memory_file.seek(0) # Rewind the BytesIO object to the beginning

    # delete_files_in_directory("./downloaded_folder")
    # delete_files_in_directory("./uploaded_folder")

    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='my_downloaded_folder.zip' # Name of the downloaded zip file
    )




@app.route("/")
def home():
    delete_files_in_directory("./downloaded_folder")
    delete_files_in_directory("./uploaded_folder")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
