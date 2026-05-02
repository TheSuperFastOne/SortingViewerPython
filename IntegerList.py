import array
import random
import time
import tkinter as tk
from collections import deque


class IntegerList:
    # These are now *virtual* animation delays, not time.sleep delays.
    # Small delays are handled by batching multiple operations per frame.
    writeDelay = 1   # ms
    accessDelay = 1  # ms

    def __init__(self, elements=None):
        if elements is None:
            elements = []

        # data is used by the algorithm.
        # visual is used by the renderer/playback.
        self.data = array.array('i', elements)
        self.visual = array.array('i', elements)

        self.ops = deque()

        # Total operations recorded by the algorithm.
        self.reads = 0
        self.writes = 0

        # Operations actually played by the animation so far.
        self.played_reads = 0
        self.played_writes = 0
        self.played_delay_ms = 0.0

        self.time_start = time.perf_counter()
        self.playback_start = None

        self.highlight_read = None
        self.highlight_write = None

    def start_recording(self):
        """Prepare to record a fresh sorting transcript."""
        self.visual = array.array('i', self.data)
        self.ops.clear()

        self.reads = 0
        self.writes = 0
        self.played_reads = 0
        self.played_writes = 0
        self.played_delay_ms = 0.0

        self.time_start = time.perf_counter()
        self.playback_start = None
        self.highlight_read = None
        self.highlight_write = None

    def start_playback(self):
        """Start the animation clock."""
        self.playback_start = time.perf_counter()
        self.time_start = self.playback_start
        self.played_reads = 0
        self.played_writes = 0
        self.played_delay_ms = 0.0
        self.highlight_read = None
        self.highlight_write = None

    def swap(self, index1, index2):
        temp = self.read(index1)
        self.write(index1, self.read(index2))
        self.write(index2, temp)

    def read(self, index):
        self.reads += 1
        self.ops.append(("read", index, self.accessDelay))
        return self.data[index]

    def write(self, index, value):
        self.writes += 1
        self.ops.append(("write", index, value, self.writeDelay))
        self.data[index] = value

    def randomize(self):
        """Shuffle immediately without counting/recording it as part of the sort."""
        for i in range(len(self.data) - 1, 0, -1):
            j = random.randint(0, i)
            self.data[i], self.data[j] = self.data[j], self.data[i]

        self.visual = array.array('i', self.data)

    def play_frame(self, max_ops_per_frame=5000):
        """
        Play all operations whose virtual delay should have elapsed by now.

        This avoids calling sleep once per operation. For tiny delays like 0.1 ms,
        several operations are batched into one frame instead of asking the OS for
        impossible sub-millisecond sleeps.
        """
        if self.playback_start is None:
            self.start_playback()

        target_delay_ms = (time.perf_counter() - self.playback_start) * 1000
        ops_played_this_frame = 0

        while self.ops and self.played_delay_ms <= target_delay_ms:
            op = self.ops.popleft()

            if op[0] == "read":
                _, index, delay_ms = op
                self.played_reads += 1
                self.played_delay_ms += delay_ms
                self.highlight_read = index
                self.highlight_write = None

            else:  # "write"
                _, index, value, delay_ms = op
                self.visual[index] = value
                self.played_writes += 1
                self.played_delay_ms += delay_ms
                self.highlight_write = index
                self.highlight_read = None

            ops_played_this_frame += 1
            if ops_played_this_frame >= max_ops_per_frame:
                break

        return not self.ops

    def Render(self, canvas: tk.Canvas):
        canvas.delete("all")
        data = self.visual
        n = len(data)
        if n == 0:
            return

        width = canvas.winfo_width()
        height = canvas.winfo_height()
        bar_width = width / n

        elapsed = time.perf_counter() - self.time_start

        canvas.create_text(
            8, 8, anchor="nw",
            text=f"Reads: {self.played_reads}/{self.reads}",
            fill="white"
        )
        canvas.create_text(
            8, 24, anchor="nw",
            text=f"Writes: {self.played_writes}/{self.writes}",
            fill="white"
        )
        canvas.create_text(
            8, 40, anchor="nw",
            text=f"Time: {elapsed:.3f}s",
            fill="white"
        )
        canvas.create_text(
            8, 56, anchor="nw",
            text=f"Delayed Time: {self.played_delay_ms / 1000:.3f}s",
            fill="white"
        )
        canvas.create_text(
            8, 72, anchor="nw",
            text=f"Queued Ops: {len(self.ops)}",
            fill="white"
        )

        for i, val in enumerate(data):
            x0 = i * bar_width + 1
            x1 = x0 + bar_width - 1
            bar_height = (val / n) * height
            y0 = height - bar_height
            y1 = height

            fill = "#4a9eff"
            if i == self.highlight_read:
                fill = "#4a9eff"
            elif i == self.highlight_write:
                fill = "#4a9eff"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="")
