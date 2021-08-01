import machine
import time
from TM1638Driver import TM1638


if __name__ == '__main__':

    board1 = TM1638(machine.Pin(5, machine.Pin.OUT),
                    machine.Pin(7, machine.Pin.OUT),
                    machine.Pin(8, machine.Pin.OUT), 1)
    board2 = TM1638(machine.Pin(6, machine.Pin.OUT),
                    machine.Pin(7, machine.Pin.OUT),
                    machine.Pin(8, machine.Pin.OUT), 1)

    board1.write_string("Test")
    board2.write_string("Test")

    seg_spin = [TM1638.SEG_TOP,
                TM1638.SEG_TOP_RIGHT,
                TM1638.SEG_BOTTOM_RIGHT,
                TM1638.SEG_BOTTOM,
                TM1638.SEG_BOTTOM_LEFT,
                TM1638.SEG_TOP_LEFT]

    while True:
        for s in seg_spin:
            board1.write_segments(7, s)
            board2.write_segments(7, s)
            time.sleep_ms(200)
