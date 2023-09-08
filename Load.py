import comtypes.client


def load_dwg_file(file_path):
    # Get running instance of AutoCAD
    acad = comtypes.client.GetActiveObject("AutoCAD.Application")

    doc = acad.Documents.Open(file_path)

    print(f"Loaded {file_path} successfully!")

if __name__ == '__main__':
    load_dwg_file("C:\\Users\\adibm\\PycharmProjects\\pythonProject1\\Drawing1.dwg")
