import tkinter as tk  
from tkinter import ttk  
import struct  
import serial  
import os  
  
def find_uart_port():  
    available_ports = [port for port in os.listdir('/dev') if port.startswith('ttyUSB') or port.startswith('ttyACM') or port.startswith('tty.usbmodem')]  
    if available_ports:  
        return '/dev/' + available_ports[0]  
    else:  
        return None  
  
def update_status(msg):  
    status_var.set(msg)  
    status_label.update_idletasks()  
  
def invia_dati():  
    try:  
        S = [[float(s_entries[i][j].get()) for j in range(3)] for i in range(4)]  
        sw1 = [int(sw1_vars[i].get()) for i in range(3)]  
        x_sp = [float(xsp_entries[i].get()) for i in range(3)]  
        PID = [[float(pid_entries[i][j].get()) for j in range(3)] for i in range(3)]  
        filtri = []  
        for idx in range(3):  
            num = [float(filtro_entries[idx][0][i].get()) for i in range(5)]  
            den = [float(filtro_entries[idx][1][i].get()) for i in range(5)]  
            filtri.extend(num)  
            filtri.extend(den)  
        sw2 = [int(sw2_vars[i].get()) for i in range(3)]  
        x_os = [float(xos_entries[i].get()) for i in range(3)]  
        D = [[float(d_entries[i][j].get()) for j in range(4)] for i in range(3)]  
  
        # Flatten all data for struct.pack  
        float_values = []  
        for row in S: float_values.extend(row)  
        float_values.extend(x_sp)  
        for row in PID: float_values.extend(row)  
        float_values.extend(filtri)  
        float_values.extend(x_os)  
        for row in D: float_values.extend(row)  
        uint8_values = sw1 + sw2  
  
        frame_format = '<' + str(len(float_values)) + 'f' + str(len(uint8_values)) + 'B'  
        frame_data = struct.pack(frame_format, *(float_values + uint8_values))  
  
        if uart_port:  
            ser = serial.Serial(uart_port, 115200, timeout=1)  
            ser.write(frame_data)  
            ser.close()  
            update_status('Data successfully sent!')  
        else:  
            update_status('No serial port found!')  
    except Exception as e:  
        update_status('Error: ' + str(e))  
  
root = tk.Tk()  
root.title('Data Sender to STM32')  
  
main_frame = ttk.Frame(root)  
main_frame.grid(row=0, column=0, padx=10, pady=10)  
  
# Left column  
col_left = ttk.Frame(main_frame)  
col_left.grid(row=0, column=0, sticky='n')  
  
# Right column  
col_right = ttk.Frame(main_frame)  
col_right.grid(row=0, column=1, sticky='n', padx=20)  
  
# Matrix S (pre-filled with 1)  
s_entries = []  
frame_s = ttk.LabelFrame(col_left, text='Matrix S')  
frame_s.grid(row=0, column=0, padx=5, pady=5)  
for i in range(4):  
    row_entries = []  
    for j in range(3):  
        e = ttk.Entry(frame_s, width=5)  
        e.insert(0, '1')  
        e.grid(row=i, column=j)  
        row_entries.append(e)  
    s_entries.append(row_entries)  
  
# Switch sw1  
sw1_vars = [tk.IntVar() for _ in range(3)]  
frame_sw1 = ttk.LabelFrame(col_left, text='Switch sw1')  
frame_sw1.grid(row=1, column=0, padx=5, pady=5)  
for i in range(3):  
    cb = ttk.Checkbutton(frame_sw1, text='sw1_' + str(i+1), variable=sw1_vars[i])  
    cb.grid(row=0, column=i)  
  
# Setpoint x_sp  
xsp_entries = []  
frame_xsp = ttk.LabelFrame(col_left, text='Setpoint x_sp')  
frame_xsp.grid(row=2, column=0, padx=5, pady=5)  
for i in range(3):  
    e = ttk.Entry(frame_xsp, width=7)  
    e.grid(row=0, column=i)  
    xsp_entries.append(e)  
  
# PID Matrix (Rows: PID, Columns: Kp, Ki, Kd)  
pid_entries = []  
frame_pid = ttk.LabelFrame(col_left, text='PID Matrix')  
frame_pid.grid(row=3, column=0, padx=5, pady=5)  
# Column headers  
ttk.Label(frame_pid, text='Kp').grid(row=0, column=1)  
ttk.Label(frame_pid, text='Ki').grid(row=0, column=2)  
ttk.Label(frame_pid, text='Kd').grid(row=0, column=3)  
for i in range(3):  
    row_entries = []  
    ttk.Label(frame_pid, text='PID ' + str(i+1)).grid(row=i+1, column=0)  
    for j in range(3):  
        e = ttk.Entry(frame_pid, width=7)  
        e.grid(row=i+1, column=j+1)  
        row_entries.append(e)  
    pid_entries.append(row_entries)  
  
# Filters (Fourth order)  
filtro_entries = []  
frame_filtri = ttk.LabelFrame(col_right, text='Fourth Order Filters')  
frame_filtri.grid(row=0, column=0, padx=5, pady=5)  
for filtro_idx in range(3):  
    subframe = ttk.LabelFrame(frame_filtri, text='Filter ' + str(filtro_idx+1))  
    subframe.grid(row=filtro_idx, column=0, padx=2, pady=2, sticky='w')  
    # Numerator  
    ttk.Label(subframe, text='Numerator:').grid(row=0, column=0, sticky='w')  
    num_entries = []  
    for i in range(5):  
        e = ttk.Entry(subframe, width=4)  
        e.grid(row=0, column=i+1)  
        num_entries.append(e)  
    # Denominator  
    ttk.Label(subframe, text='Denominator:').grid(row=1, column=0, sticky='w')  
    den_entries = []  
    for i in range(5):  
        e = ttk.Entry(subframe, width=4)  
        e.grid(row=1, column=i+1)  
        den_entries.append(e)  
    filtro_entries.append((num_entries, den_entries))  
  
# Switch sw2  
sw2_vars = [tk.IntVar() for _ in range(3)]  
frame_sw2 = ttk.LabelFrame(col_right, text='Switch sw2')  
frame_sw2.grid(row=1, column=0, padx=5, pady=5)  
for i in range(3):  
    cb = ttk.Checkbutton(frame_sw2, text='sw2_' + str(i+1), variable=sw2_vars[i])  
    cb.grid(row=0, column=i)  
  
# Offset x_os  
xos_entries = []  
frame_xos = ttk.LabelFrame(col_right, text='Offset x_os')  
frame_xos.grid(row=2, column=0, padx=5, pady=5)  
for i in range(3):  
    e = ttk.Entry(frame_xos, width=7)  
    e.grid(row=0, column=i)  
    xos_entries.append(e)  
  
# Matrix D (pre-filled with 1)  
d_entries = []  
frame_d = ttk.LabelFrame(col_right, text='Matrix D')  
frame_d.grid(row=3, column=0, padx=5, pady=5)  
for i in range(3):  
    row_entries = []  
    for j in range(4):  
        e = ttk.Entry(frame_d, width=5)  
        e.insert(0, '1')  
        e.grid(row=i, column=j)  
        row_entries.append(e)  
    d_entries.append(row_entries)  
  
# Status box (white text)  
status_var = tk.StringVar()  
status_label = tk.Label(main_frame, textvariable=status_var, bg='black', fg='white', relief='sunken', anchor='w', width=50)  
status_label.grid(row=2, column=0, columnspan=2, pady=10, sticky='we')  
  
# Send button  
ttk.Button(main_frame, text='Send Data', command=invia_dati).grid(row=1, column=0, columnspan=2, pady=15)  
  
# Serial port detection at startup  
uart_port = find_uart_port()  
if uart_port:  
    update_status('Serial port found: ' + uart_port)  
else:  
    update_status('No serial port found!')  
  
root.mainloop()  