import tkinter as tk
from IntegerList import IntegerList
from listSorter import bubbleSort, shaker


SORT_ALGORITHM = bubbleSort
# SORT_ALGORITHM = shaker


def main():
    root = tk.Tk()
    root.title("Sorting Visualizer")

    canvas = tk.Canvas(root, width=800, height=800, bg="black")
    canvas.pack()

    lst = IntegerList(list(range(1, 70)))
    lst.randomize()

    # Record the sort immediately, with no sleeping and no GUI blocking.
    lst.start_recording()
    SORT_ALGORITHM(lst)

    # Now animate the recorded transcript.
    lst.start_playback()

    def render_loop():
        done = lst.play_frame()
        lst.Render(canvas)

        if not done:
            root.after(16, render_loop)  # about 60 FPS
        else:
            # One final render with all operations applied.
            lst.Render(canvas)

    render_loop()
    root.mainloop()


if __name__ == "__main__":
    main()
