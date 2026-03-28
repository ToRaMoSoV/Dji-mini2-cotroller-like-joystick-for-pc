import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import serial
import threading
import time
import struct
import pyxinput

def calc_checksum(packet, plength):
    crc = [0x0000, 0x1189, 0x2312, 0x329b, 0x4624, 0x57ad, 0x6536, 0x74bf,
           0x8c48, 0x9dc1, 0xaf5a, 0xbed3, 0xca6c, 0xdbe5, 0xe97e, 0xf8f7,
           0x1081, 0x0108, 0x3393, 0x221a, 0x56a5, 0x472c, 0x75b7, 0x643e,
           0x9cc9, 0x8d40, 0xbfdb, 0xae52, 0xdaed, 0xcb64, 0xf9ff, 0xe876,
           0x2102, 0x308b, 0x0210, 0x1399, 0x6726, 0x76af, 0x4434, 0x55bd,
           0xad4a, 0xbcc3, 0x8e58, 0x9fd1, 0xeb6e, 0xfae7, 0xc87c, 0xd9f5,
           0x3183, 0x200a, 0x1291, 0x0318, 0x77a7, 0x662e, 0x54b5, 0x453c,
           0xbdcb, 0xac42, 0x9ed9, 0x8f50, 0xfbef, 0xea66, 0xd8fd, 0xc974,
           0x4204, 0x538d, 0x6116, 0x709f, 0x0420, 0x15a9, 0x2732, 0x36bb,
           0xce4c, 0xdfc5, 0xed5e, 0xfcd7, 0x8868, 0x99e1, 0xab7a, 0xbaf3,
           0x5285, 0x430c, 0x7197, 0x601e, 0x14a1, 0x0528, 0x37b3, 0x263a,
           0xdecd, 0xcf44, 0xfddf, 0xec56, 0x98e9, 0x8960, 0xbbfb, 0xaa72,
           0x6306, 0x728f, 0x4014, 0x519d, 0x2522, 0x34ab, 0x0630, 0x17b9,
           0xef4e, 0xfec7, 0xcc5c, 0xddd5, 0xa96a, 0xb8e3, 0x8a78, 0x9bf1,
           0x7387, 0x620e, 0x5095, 0x411c, 0x35a3, 0x242a, 0x16b1, 0x0738,
           0xffcf, 0xee46, 0xdcdd, 0xcd54, 0xb9eb, 0xa862, 0x9af9, 0x8b70,
           0x8408, 0x9581, 0xa71a, 0xb693, 0xc22c, 0xd3a5, 0xe13e, 0xf0b7,
           0x0840, 0x19c9, 0x2b52, 0x3adb, 0x4e64, 0x5fed, 0x6d76, 0x7cff,
           0x9489, 0x8500, 0xb79b, 0xa612, 0xd2ad, 0xc324, 0xf1bf, 0xe036,
           0x18c1, 0x0948, 0x3bd3, 0x2a5a, 0x5ee5, 0x4f6c, 0x7df7, 0x6c7e,
           0xa50a, 0xb483, 0x8618, 0x9791, 0xe32e, 0xf2a7, 0xc03c, 0xd1b5,
           0x2942, 0x38cb, 0x0a50, 0x1bd9, 0x6f66, 0x7eef, 0x4c74, 0x5dfd,
           0xb58b, 0xa402, 0x9699, 0x8710, 0xf3af, 0xe226, 0xd0bd, 0xc134,
           0x39c3, 0x284a, 0x1ad1, 0x0b58, 0x7fe7, 0x6e6e, 0x5cf5, 0x4d7c,
           0xc60c, 0xd785, 0xe51e, 0xf497, 0x8028, 0x91a1, 0xa33a, 0xb2b3,
           0x4a44, 0x5bcd, 0x6956, 0x78df, 0x0c60, 0x1de9, 0x2f72, 0x3efb,
           0xd68d, 0xc704, 0xf59f, 0xe416, 0x90a9, 0x8120, 0xb3bb, 0xa232,
           0x5ac5, 0x4b4c, 0x79d7, 0x685e, 0x1ce1, 0x0d68, 0x3ff3, 0x2e7a,
           0xe70e, 0xf687, 0xc41c, 0xd595, 0xa12a, 0xb0a3, 0x8238, 0x93b1,
           0x6b46, 0x7acf, 0x4854, 0x59dd, 0x2d62, 0x3ceb, 0x0e70, 0x1ff9,
           0xf78f, 0xe606, 0xd49d, 0xc514, 0xb1ab, 0xa022, 0x92b9, 0x8330,
           0x7bc7, 0x6a4e, 0x58d5, 0x495c, 0x3de3, 0x2c6a, 0x1ef1, 0x0f78]
    v = 0x3692
    for i in range(plength):
        vv = v >> 8
        v = vv ^ crc[((packet[i] ^ v) & 0xFF)]
    return v

def calc_pkt55_hdr_checksum(seed, packet, plength):
    arr_2A103 = [0x00,0x5E,0xBC,0xE2,0x61,0x3F,0xDD,0x83,0xC2,0x9C,0x7E,0x20,0xA3,0xFD,0x1F,0x41,
                 0x9D,0xC3,0x21,0x7F,0xFC,0xA2,0x40,0x1E,0x5F,0x01,0xE3,0xBD,0x3E,0x60,0x82,0xDC,
                 0x23,0x7D,0x9F,0xC1,0x42,0x1C,0xFE,0xA0,0xE1,0xBF,0x5D,0x03,0x80,0xDE,0x3C,0x62,
                 0xBE,0xE0,0x02,0x5C,0xDF,0x81,0x63,0x3D,0x7C,0x22,0xC0,0x9E,0x1D,0x43,0xA1,0xFF,
                 0x46,0x18,0xFA,0xA4,0x27,0x79,0x9B,0xC5,0x84,0xDA,0x38,0x66,0xE5,0xBB,0x59,0x07,
                 0xDB,0x85,0x67,0x39,0xBA,0xE4,0x06,0x58,0x19,0x47,0xA5,0xFB,0x78,0x26,0xC4,0x9A,
                 0x65,0x3B,0xD9,0x87,0x04,0x5A,0xB8,0xE6,0xA7,0xF9,0x1B,0x45,0xC6,0x98,0x7A,0x24,
                 0xF8,0xA6,0x44,0x1A,0x99,0xC7,0x25,0x7B,0x3A,0x64,0x86,0xD8,0x5B,0x05,0xE7,0xB9,
                 0x8C,0xD2,0x30,0x6E,0xED,0xB3,0x51,0x0F,0x4E,0x10,0xF2,0xAC,0x2F,0x71,0x93,0xCD,
                 0x11,0x4F,0xAD,0xF3,0x70,0x2E,0xCC,0x92,0xD3,0x8D,0x6F,0x31,0xB2,0xEC,0x0E,0x50,
                 0xAF,0xF1,0x13,0x4D,0xCE,0x90,0x72,0x2C,0x6D,0x33,0xD1,0x8F,0x0C,0x52,0xB0,0xEE,
                 0x32,0x6C,0x8E,0xD0,0x53,0x0D,0xEF,0xB1,0xF0,0xAE,0x4C,0x12,0x91,0xCF,0x2D,0x73,
                 0xCA,0x94,0x76,0x28,0xAB,0xF5,0x17,0x49,0x08,0x56,0xB4,0xEA,0x69,0x37,0xD5,0x8B,
                 0x57,0x09,0xEB,0xB5,0x36,0x68,0x8A,0xD4,0x95,0xCB,0x29,0x77,0xF4,0xAA,0x48,0x16,
                 0xE9,0xB7,0x55,0x0B,0x88,0xD6,0x34,0x6A,0x2B,0x75,0x97,0xC9,0x4A,0x14,0xF6,0xA8,
                 0x74,0x2A,0xC8,0x96,0x15,0x4B,0xA9,0xF7,0xB6,0xE8,0x0A,0x54,0xD7,0x89,0x6B,0x35]
    chksum = seed
    for i in range(plength):
        chksum = arr_2A103[((packet[i] ^ chksum) & 0xFF)]
    return chksum

def send_duml(s, source, target, cmd_type, cmd_set, cmd_id, payload=None):
    global sequence_number
    sequence_number = 0x34eb
    packet = bytearray.fromhex('55')
    length = 13
    if payload is not None:
        length += len(payload)

    if length > 0x3ff:
        raise ValueError("Packet too large")

    packet += struct.pack('B', length & 0xff)
    packet += struct.pack('B', (length >> 8) | 0x4)
    hdr_crc = calc_pkt55_hdr_checksum(0x77, packet, 3)
    packet += struct.pack('B', hdr_crc)
    packet += struct.pack('B', source)
    packet += struct.pack('B', target)
    packet += struct.pack('<H', sequence_number)
    packet += struct.pack('B', cmd_type)
    packet += struct.pack('B', cmd_set)
    packet += struct.pack('B', cmd_id)

    if payload is not None:
        packet += payload

    crc = calc_checksum(packet, len(packet))
    packet += struct.pack('<H', crc)
    s.write(packet)
    sequence_number += 1

class RC2Xbox:
    def __init__(self, root):
        self.root = root
        self.root.title("DJI Mini 2 RC to Xbox Controller")
        self.root.geometry("900x700")

        self.serial = None
        self.running = False
        self.emulating = False
        self.calibration = {
            'lh': {'min': 364, 'center': 1024, 'max': 1684},
            'lv': {'min': 364, 'center': 1024, 'max': 1684},
            'rh': {'min': 364, 'center': 1024, 'max': 1684},
            'rv': {'min': 364, 'center': 1024, 'max': 1684},
            'wheel': {'min': 364, 'center': 1024, 'max': 1684}
        }
        self.current = {'lh': 0, 'lv': 0, 'rh': 0, 'rv': 0, 'wheel': 0,
                        'fn': 0, 'camera_mode': 0, 'shutter': 0, 'home': 0,
                        'speed_mode': 0, 't1': 0}

        self.xbox = None

        self.create_widgets()

        self.serial_thread = None
        self.update_gui_running = True
        self.gui_update_interval = 16
        self.schedule_gui_update()

    def create_widgets(self):
        top_frame = ttk.LabelFrame(self.root, text="Control", padding=10)
        top_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(top_frame, text="COM Port:").grid(row=0, column=0, sticky='w', padx=5)
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(top_frame, textvariable=self.port_var, values=self.list_ports())
        self.port_combo.grid(row=0, column=1, padx=5, pady=5)

        self.connect_btn = ttk.Button(top_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=2, padx=5)

        self.calibrate_btn = ttk.Button(top_frame, text="Calibrate", command=self.start_calibration, state='disabled')
        self.calibrate_btn.grid(row=0, column=3, padx=5)

        self.emulate_btn = ttk.Button(top_frame, text="Start Emulation", command=self.toggle_emulation, state='disabled')
        self.emulate_btn.grid(row=0, column=4, padx=5)

        self.status_label = ttk.Label(top_frame, text="Disconnected")
        self.status_label.grid(row=0, column=5, padx=10)

        values_frame = ttk.LabelFrame(self.root, text="Current Stick Values", padding=10)
        values_frame.pack(fill='x', padx=10, pady=5)

        self.value_vars = {}
        labels = [('Left X', 'lh'), ('Left Y', 'lv'), ('Right X', 'rh'), ('Right Y', 'rv'),
                  ('Wheel', 'wheel'),
                  ('FN', 'fn'), ('Camera Mode', 'camera_mode'), ('Shutter', 'shutter'), ('Home', 'home'),
                  ('Speed Mode', 'speed_mode')]
        for i, (text, key) in enumerate(labels):
            ttk.Label(values_frame, text=text+":").grid(row=i//4, column=(i%4)*2, sticky='e', padx=5)
            var = tk.StringVar(value="0")
            self.value_vars[key] = var
            ttk.Label(values_frame, textvariable=var).grid(row=i//4, column=(i%4)*2+1, sticky='w', padx=5)

        graph_frame = ttk.Frame(self.root)
        graph_frame.pack(fill='both', expand=True, padx=10, pady=5)

        left_fig = Figure(figsize=(4, 4), dpi=100)
        self.left_ax = left_fig.add_subplot(111)
        self.left_ax.set_title("Left Stick")
        self.left_ax.set_xlim(-1, 1)
        self.left_ax.set_ylim(-1, 1)
        self.left_ax.grid(True)
        self.left_point, = self.left_ax.plot(0, 0, 'ro', markersize=8)
        self.left_canvas = FigureCanvasTkAgg(left_fig, master=graph_frame)
        self.left_canvas.get_tk_widget().pack(side='left', fill='both', expand=True)

        right_fig = Figure(figsize=(4, 4), dpi=100)
        self.right_ax = right_fig.add_subplot(111)
        self.right_ax.set_title("Right Stick")
        self.right_ax.set_xlim(-1, 1)
        self.right_ax.set_ylim(-1, 1)
        self.right_ax.grid(True)
        self.right_point, = self.right_ax.plot(0, 0, 'bo', markersize=8)
        self.right_canvas = FigureCanvasTkAgg(right_fig, master=graph_frame)
        self.right_canvas.get_tk_widget().pack(side='right', fill='both', expand=True)

    def list_ports(self):
        import serial.tools.list_ports
        return [port.device for port in serial.tools.list_ports.comports()]

    def toggle_connection(self):
        if self.serial is None:
            port = self.port_var.get()
            if not port:
                messagebox.showerror("Error", "Please select a COM port.")
                return
            try:
                self.serial = serial.Serial(port=port, baudrate=115200, timeout=0.1)
                self.status_label.config(text="Connected to "+port)
                self.connect_btn.config(text="Disconnect")
                self.calibrate_btn.config(state='normal')
                self.emulate_btn.config(state='normal')
                self.running = True
                self.serial_thread = threading.Thread(target=self.serial_reader, daemon=True)
                self.serial_thread.start()
                try:
                    send_duml(self.serial, 0x0a, 0x06, 0x40, 0x06, 0x24, bytearray.fromhex('01'))
                except Exception as e:
                    print("Failed to send simulator enable:", e)
            except Exception as e:
                messagebox.showerror("Connection Error", str(e))
                self.serial = None
        else:
            self.running = False
            if self.serial_thread and self.serial_thread.is_alive():
                self.serial_thread.join(timeout=1)
            self.serial.close()
            self.serial = None
            self.status_label.config(text="Disconnected")
            self.connect_btn.config(text="Connect")
            self.calibrate_btn.config(state='disabled')
            self.emulate_btn.config(state='disabled')
            if self.emulating:
                self.toggle_emulation()

    def start_calibration(self):
        if not self.serial:
            return
        was_emulating = self.emulating
        if was_emulating:
            self.toggle_emulation()
        self.running = False
        if self.serial_thread and self.serial_thread.is_alive():
            self.serial_thread.join(timeout=1)
        cal = CalibrationDialog(self.root, self.serial)
        if cal.result:
            self.calibration = cal.result
        self.running = True
        self.serial_thread = threading.Thread(target=self.serial_reader, daemon=True)
        self.serial_thread.start()
        if was_emulating:
            self.toggle_emulation()

    def toggle_emulation(self):
        if not self.emulating:
            try:
                self.xbox = pyxinput.vController()
                self.emulating = True
                self.emulate_btn.config(text="Stop Emulation")
                self.status_label.config(text="Emulating Xbox Controller")
            except Exception as e:
                messagebox.showerror("Emulation Error", f"Could not start emulation:\n{e}\n\nMake sure vJoy is installed and configured.")
                return
        else:
            self.emulating = False
            self.xbox = None
            self.emulate_btn.config(text="Start Emulation")
            self.status_label.config(text="Connected" if self.serial else "Disconnected")

    def serial_reader(self):
        while self.running and self.serial and self.serial.is_open:
            try:
                send_duml(self.serial, 0x0a, 0x06, 0x40, 0x06, 0x01, bytearray.fromhex(''))
                send_duml(self.serial, 0x0a, 0x06, 0x40, 0x06, 0x27, bytearray.fromhex(''))

                while True:
                    b = self.serial.read(1)
                    if not b:
                        break
                    if b == b'\x55':
                        ph = self.serial.read(2)
                        if len(ph) != 2:
                            break
                        pl = (ph[0] & 0xFF) | ((ph[1] & 0x03) << 8)
                        pc = self.serial.read(1)
                        if len(pc) != 1:
                            break
                        pd = self.serial.read(pl - 4)
                        if len(pd) != pl - 4:
                            break
                        data = b'\x55' + ph + pc + pd
                        self.process_packet(data)
                        break
            except Exception as e:
                print("Serial read error:", e)
                time.sleep(0.05)

    def process_packet(self, packet):
        if len(packet) == 38:
            lh = int.from_bytes(packet[22:24], 'little')
            lv = int.from_bytes(packet[19:21], 'little')
            rh = int.from_bytes(packet[13:15], 'little')
            rv = int.from_bytes(packet[16:18], 'little')
            wheel_raw = int.from_bytes(packet[25:27], 'little')

            self.current['lh'] = self.map_stick(lh, 'lh')
            self.current['lv'] = self.map_stick(lv, 'lv')
            self.current['rh'] = self.map_stick(rh, 'rh')
            self.current['rv'] = self.map_stick(rv, 'rv')
            self.current['wheel'] = self.map_stick(wheel_raw, 'wheel')

        elif len(packet) == 58:
            buttons_raw = int.from_bytes(packet[28:30], 'big')
            self.current['fn'] = 1 if buttons_raw & 0x0002 else 0
            self.current['camera_mode'] = 1 if buttons_raw & 0x0004 else 0
            self.current['shutter'] = 1 if (buttons_raw & 0x0060) == 0x0060 else 0
            self.current['home'] = 1 if buttons_raw & 0x0080 else 0

            wheel_btn_raw = int.from_bytes(packet[27:29], 'big')
            if wheel_btn_raw == 0x0:
                self.current['t1'] = 1.0
                self.current['speed_mode'] = 2
            elif wheel_btn_raw & 0x20:
                self.current['t1'] = -1.0
                self.current['speed_mode'] = 0
            else:
                self.current['t1'] = 0.0
                self.current['speed_mode'] = 1

        if self.emulating and self.xbox:
            lx = self.current['lh']
            ly = self.current['lv']
            rx = self.current['rh']
            ry = -self.current['rv']
            lt = (self.current['t1'] + 1) / 2 if self.current.get('t1') is not None else 0.0
            rt = (self.current['wheel'] + 1) / 2

            self.xbox.set_value('AxisLx', lx)
            self.xbox.set_value('AxisLy', ly)
            self.xbox.set_value('AxisRx', rx)
            self.xbox.set_value('AxisRy', ry)
            self.xbox.set_value('TriggerL', lt)
            self.xbox.set_value('TriggerR', rt)

            self.xbox.set_value('BtnA', self.current['fn'])
            self.xbox.set_value('BtnB', self.current['camera_mode'])
            self.xbox.set_value('BtnX', self.current['shutter'])
            self.xbox.set_value('BtnY', self.current['home'])

    def map_stick(self, raw, axis):
        cal = self.calibration[axis]
        if raw < cal['center']:
            return -1.0 + (raw - cal['min']) / (cal['center'] - cal['min'])
        elif raw > cal['center']:
            return (raw - cal['center']) / (cal['max'] - cal['center'])
        else:
            return 0.0

    def schedule_gui_update(self):
        if self.update_gui_running:
            self.update_gui()
            self.root.after(self.gui_update_interval, self.schedule_gui_update)

    def update_gui(self):
        for key, var in self.value_vars.items():
            val = self.current.get(key, 0)
            if isinstance(val, float):
                var.set(f"{val:.3f}")
            else:
                var.set(str(val))

        lx = self.current.get('lh', 0)
        ly = self.current.get('lv', 0)
        self.left_point.set_data([lx], [ly])
        self.left_canvas.draw_idle()

        rx = self.current.get('rh', 0)
        ry = self.current.get('rv', 0)
        self.right_point.set_data([rx], [ry])
        self.right_canvas.draw_idle()

    def on_closing(self):
        self.update_gui_running = False
        self.running = False
        if self.serial and self.serial.is_open:
            self.serial.close()
        if self.emulating:
            self.toggle_emulation()
        self.root.destroy()

class CalibrationDialog(tk.Toplevel):
    def __init__(self, parent, serial):
        super().__init__(parent)
        self.title("Calibrate Sticks")
        self.geometry("500x400")
        self.serial = serial
        self.result = None

        self.instructions = ttk.Label(self, text="Move each stick to extremes and center.\nClick 'Start' when ready.")
        self.instructions.pack(pady=10)

        self.start_btn = ttk.Button(self, text="Start Calibration", command=self.start_calibration)
        self.start_btn.pack(pady=5)

        self.progress = ttk.Progressbar(self, mode='indeterminate')
        self.status = ttk.Label(self, text="")
        self.current_axis = None
        self.samples = {axis: [] for axis in ['lh', 'lv', 'rh', 'rv', 'wheel']}
        self.stage = 0
        self.axes = ['lh', 'lv', 'rh', 'rv', 'wheel']

    def start_calibration(self):
        self.start_btn.config(state='disabled')
        self.progress.pack(fill='x', padx=20, pady=5)
        self.status.pack(pady=5)
        self.progress.start(10)
        self.calibrate_next_axis()

    def calibrate_next_axis(self):
        if self.stage >= len(self.axes):
            self.progress.stop()
            self.status.config(text="Calibration finished.")
            self.result = self.build_calibration()
            self.destroy()
            return

        axis = self.axes[self.stage]
        self.status.config(text=f"Calibrating {axis}. Move stick to full left/up, full right/down, and center. Press any key when done.")
        self.current_axis = axis
        self.samples[axis] = []
        self.collect_samples()

    def collect_samples(self):
        timeout = time.time() + 5.0
        while time.time() < timeout:
            try:
                send_duml(self.serial, 0x0a, 0x06, 0x40, 0x06, 0x01, bytearray.fromhex(''))
                b = self.serial.read(1)
                if b == b'\x55':
                    ph = self.serial.read(2)
                    if len(ph) != 2:
                        continue
                    pl = (ph[0] & 0xFF) | ((ph[1] & 0x03) << 8)
                    pc = self.serial.read(1)
                    if len(pc) != 1:
                        continue
                    pd = self.serial.read(pl - 4)
                    if len(pd) != pl - 4:
                        continue
                    packet = b'\x55' + ph + pc + pd
                    if len(packet) == 38:
                        lh = int.from_bytes(packet[22:24], 'little')
                        lv = int.from_bytes(packet[19:21], 'little')
                        rh = int.from_bytes(packet[13:15], 'little')
                        rv = int.from_bytes(packet[16:18], 'little')
                        wheel_raw = int.from_bytes(packet[25:27], 'little')
                        values = {'lh': lh, 'lv': lv, 'rh': rh, 'rv': rv, 'wheel': wheel_raw}
                        self.samples[self.current_axis].append(values[self.current_axis])
            except Exception as e:
                print("Calibration read error:", e)
            time.sleep(0.01)

        if self.samples[self.current_axis]:
            min_val = min(self.samples[self.current_axis])
            max_val = max(self.samples[self.current_axis])
            center_val = sum(self.samples[self.current_axis]) / len(self.samples[self.current_axis])
            self.samples[self.current_axis] = {'min': min_val, 'center': center_val, 'max': max_val}
        else:
            self.samples[self.current_axis] = {'min': 364, 'center': 1024, 'max': 1684}

        self.status.config(text=f"{self.current_axis} done. Min={self.samples[self.current_axis]['min']}, Center={self.samples[self.current_axis]['center']:.0f}, Max={self.samples[self.current_axis]['max']}")
        self.stage += 1
        self.after(1000, self.calibrate_next_axis)

    def build_calibration(self):
        return {
            'lh': self.samples['lh'],
            'lv': self.samples['lv'],
            'rh': self.samples['rh'],
            'rv': self.samples['rv'],
            'wheel': self.samples['wheel']
        }

if __name__ == "__main__":
    root = tk.Tk()
    app = RC2Xbox(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
