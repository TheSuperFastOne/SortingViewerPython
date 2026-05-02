import array
import time
import tkinter as tk
from IntegerList import IntegerList
from listSorter import bubbleSort, shaker, selectionSort 
from listSorter import insertionSort, gnomeSort, oddEvenSort, combSort


def benchmarkFunctionQuadratic(func, trials):
    results = {}
    for n in range(1000, 50000, 1000):
        lst = IntegerList([round(i * i / n) for i in range(1, n)])
        lst.randomize()
        total = 0
        for i in range(0, trials):
            func(lst)
            total += lst.reads * lst.readDelay + lst.writes * lst.writeDelay
            lst.randomize()
        results[n] = total / trials
    return results
        


def main_benchmark():
    func = combSort
    trials = 3

def main_render():
    func = combSort
    root = tk.Tk()
    root.title("Sorting Visualizer")

    canvas = tk.Canvas(root, width=1400, height=800, bg="black")
    canvas.pack()

    n = 500
    lst = IntegerList([round(i * i / n) for i in range(1, n)])
    lst.randomize()

    # First, record the whole sort instantly.
    func(lst)

    # Reset displayed data to the randomized starting state.

    lst.time_start = time.perf_counter()

    def playback_loop():
        # Play several operations per frame so it is not painfully slow.
        ops_per_frame = 200

        used_ops = 0

        while used_ops < ops_per_frame:
            cost = lst.play_next_op()

            if cost == 0:
                lst.Render(canvas)
                return

            used_ops += cost

        lst.Render(canvas)
        root.after(16, playback_loop)

    playback_loop()
    root.mainloop()


if __name__ == "__main__":
    main_render()
