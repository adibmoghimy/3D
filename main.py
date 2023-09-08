import ezdxf



def print_hi(name):
    total_types = set()

    doc = ezdxf.readfile("Drawing1.dxf")
    mspace = doc.modelspace()
    for entity in mspace:
        total_types.add(entity.dxftype())

    print(total_types)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
