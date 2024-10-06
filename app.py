from tkinter import Tk
from models import MainWindow


def main():

    # Main window
    root = Tk()

    # Creates a MainWindow-class object
    MainWindow(root)

    # Avoids window to be closed
    root.mainloop()


if __name__ == '__main__':
    main()
