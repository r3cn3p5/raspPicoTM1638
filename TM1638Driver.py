import sevenSegFont


class TM1638:
    READ_MODE = 0x02
    WRITE_MODE = 0x00
    INCR_ADDR = 0x00
    FIXED_ADDR = 0x04

    SEG_TOP = 0x01
    SEG_TOP_LEFT = 0x20
    SEG_BOTTOM_RIGHT = 0x04
    SEG_BOTTOM = 0x08
    SEG_BOTTOM_LEFT = 0x10
    SEG_TOP_RIGHT = 0x02
    SEG_MIDDLE = 0x40
    SEG_DP = 0x80

    KEY_1 = 0x01
    KEY_2 = 0x02
    KEY_3 = 0x04
    KEY_4 = 0x08
    KEY_5 = 0x10
    KEY_6 = 0x20
    KEY_7 = 0x40
    KEY_8 = 0x80

    def __init__(self, stb, clk, dio, brightness):
        self.stb = stb
        self.clk = clk
        self.dio = dio

        self.stb.value(False)
        self._send_byte(0x40 | TM1638.WRITE_MODE | TM1638.INCR_ADDR)
        self._send_byte(0xC0)  # address command set to the 1st address
        for _ in range(16):
            self._send_byte(0x00)  # set to zero all the addresses
        self.stb.value(True)

        self.stb.value(False)
        self._send_byte(0x88 | (brightness & 7))
        self.stb.value(True)

    def write_string(self, display_str):

        c_loc = 0
        for i in range(8):
            if c_loc < len(display_str)-1 and display_str[c_loc+1] == '.':
                self.send_data(i * 2, sevenSegFont.FONT[display_str[c_loc]] | TM1638.SEG_DP)
                c_loc += 1
            elif c_loc < len(display_str):
                self.send_data(i * 2, sevenSegFont.FONT[display_str[c_loc]])
            else:
                self.send_data(i * 2, 0)
            c_loc += 1

    def write_character(self, position, character, dot=False):
        self.stb.value(False)
        if dot:
            self.send_data(position * 2, sevenSegFont.FONT[character] | TM1638.SEG_DP)
        else:
            self.send_data(position * 2, sevenSegFont.FONT[character])
        self.stb.value(True)

    def write_segments(self, position, byte):
        self.stb.value(False)
        self.send_data(position * 2, byte)
        self.stb.value(True)

    def toggle_led(self, position, state):
        self.stb.value(False)
        self.send_data(position * 2 + 1, state)
        self.stb.value(True)

    def read_keys(self):
        in_bytes = self.get_data()

        key = 0
        if in_bytes[0] & 1 == 1:
            key |= TM1638.KEY_1
        if in_bytes[0] & 16 == 16:
            key |= TM1638.KEY_5
        if in_bytes[1] & 1 == 1:
            key |= TM1638.KEY_2
        if in_bytes[1] & 16 == 16:
            key |= TM1638.KEY_6
        if in_bytes[2] & 1 == 1:
            key |= TM1638.KEY_3
        if in_bytes[2] & 16 == 16:
            key |= TM1638.KEY_7
        if in_bytes[3] & 1 == 1:
            key |= TM1638.KEY_4
        if in_bytes[3] & 16 == 16:
            key |= TM1638.KEY_8

        return key

    def send_data(self, addr, data):
        # set mode
        self.stb.value(False)
        self._send_byte(0x40 | TM1638.WRITE_MODE | TM1638.FIXED_ADDR)
        self.stb.value(True)

        # set address and send byte (stb must go high and low before sending address)
        self.stb.value(False)
        self._send_byte(0xC0 | addr)
        self._send_byte(data)
        self.stb.value(True)

    def get_data(self):
        self.stb.value(False)
        self._send_byte(0x40 | TM1638.READ_MODE | TM1638.INCR_ADDR)

        b = []
        for _ in range(4):
            b.append(self._get_byte())
        self.stb.value(True)
        return b

    def _send_byte(self, data):
        for _ in range(8):
            self.clk.low()
            self.dio.value((data & 1) == 1)
            data >>= 1
            self.clk.high()

    def _get_byte(self):

        self.dio.init(self.dio.IN, self.dio.PULL_DOWN)
        # read 8 bits
        temp = 0
        for _ in range(8):
            temp >>= 1
            self.clk.low()
            if self.dio.value():
                temp |= 0x80
            self.clk.high()
        # put back DIO in output mode
        self.dio.init(self.dio.OUT, self.dio.PULL_DOWN)

        return temp
