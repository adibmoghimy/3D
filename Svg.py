import ezdxf
import matplotlib.pyplot as plt


# Load the DWG file
def save_svg():
    # Load the DWG file
    doc = ezdxf.readfile("1.dxf")

    # Create a new figure
    fig, ax = plt.subplots()

    # Add entities from the DWG file to the figure
    msp = doc.modelspace()
    for entity in msp:
        if entity.dxftype() == 'LINE':
            ax.plot([entity.dxf.start[0], entity.dxf.end[0]], [entity.dxf.start[1], entity.dxf.end[1]], color='black')

    # Set the aspect ratio to be equal
    ax.set_aspect('equal')

    # Save the figure as an SVG file
    plt.savefig("output.svg")


if __name__ == '__main__':
    save_svg()
