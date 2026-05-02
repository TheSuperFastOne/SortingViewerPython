import array
import random
import time
import tkinter as tk


class IntegerList:
    writeDelay = 1.4  # operations
    readDelay = 1  # operations

    writes = 0
    reads = 0

    def __init__(self, elements=None):
        if elements is None:
            elements = []
        self.data = array.array('i', elements)
        self.visual = array.array('i', elements)

        self.ops = []
        self.writes = 0
        self.reads = 0
        self.playback_reads = 0
        self.playback_writes = 0
        self.time_start = time.perf_counter()


    def swap(self, index1, index2):
        temp = self.read(index1)
        self.write(index1, self.read(index2))
        self.write(index2, temp)

    def read(self, index):
        self.ops.append(("read", index))
        self.reads += 1
        return self.data[index]

    def write(self, index, value):
        self.ops.append(("write", index, value))
        self.writes += 1
        self.data[index] = value
    
    def play_next_op(self):
        if not self.ops:
            return False

        op = self.ops.pop(0)

        if op[0] == "read":
            self.playback_reads += 1
            return self.readDelay

        elif op[0] == "write":
            _, index, value = op
            self.visual[index] = value
            self.playback_writes += 1
            return self.writeDelay


    def randomize(self):
        for i in range(len(self.data) - 1, 0, -1):
            j = random.randint(0, i)
            self.data[i], self.data[j] = self.data[j], self.data[i]

        self.visual = array.array('i', self.data)
        self.ops.clear()

        self.reads = 0
        self.writes = 0
        self.playback_reads = 0
        self.playback_writes = 0

    def Render(self, canvas: tk.Canvas):
        canvas.delete("all")
        data = self.visual
        n = len(data)
        if n == 0:
            return

        width = canvas.winfo_width()
        height = canvas.winfo_height()
        bar_width = width / n

        canvas.create_text(8, 8,  anchor="nw", text=f"Reads: {self.playback_reads}",  fill="white")
        canvas.create_text(8, 24, anchor="nw", text=f"Writes: {self.playback_writes}", fill="white")
        canvas.create_text(8, 40, anchor="nw", text=f"Time: {(time.perf_counter() - self.time_start):.3f}", fill="white")

        for i, val in enumerate(data):
            x0 = i * bar_width + 1
            x1 = x0 + bar_width
            bar_height = (val / n) * height
            y0 = height - bar_height
            y1 = height
            canvas.create_rectangle(x0, y0, x1, y1, fill="#4a9eff", outline="")
