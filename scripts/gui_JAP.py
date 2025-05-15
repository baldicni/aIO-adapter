import tkinter as tk  
from tkinter import ttk  
import struct  
import serial  
import os  
import numpy as np
from scipy.signal import sos2zpk, iirfilter, tf2sos, iirnotch



''' 
SCRIPT FILTER DESIGN
BEGIN

'''

def filter_design(f0, fs=1000, Q=None, order=4, type=None):
    
    if type == 'notch' and Q is not None:
        b, a = iirnotch(f0, Q, fs)
        order = 1
    else:
        b,a = iirfilter(N = order, Wn = f0, fs=fs, btype=type, ftype='butter', output='ba')
    sos = tf2sos(b, a)
    z, p, k = sos2zpk(sos)  # zeros, poles, gain

    #Stability check: all poles must have magnitude < 1
    #is_stable = all(abs(pole) < 1 for pole in p)
    #print(np.sort(np.abs(p)))
    #print("The filter is Stable." if is_stable else "The filter is Unstable.")

    # Convert to CMSIS format: Coefficients of the feedback part, a_1 and a_2, has to be negated as indicated in the arm_biquad_cascade_df1_f32 function
    cmsis_coefs=np.reshape(np.hstack((sos[:,:3],-sos[:,4:])),int(5*np.ceil(order/2)))
    return cmsis_coefs

'''
END
 '''
  
def find_uart_port():  
    available_ports = [port for port in os.listdir('/dev') if port.startswith('ttyUSB') or port.startswith('ttyACM') or port.startswith('tty.usbmodem')]  
    if available_ports:  
        return '/dev/' + available_ports[0]  
    else:  
        return None  
  
def update_status(msg, frame, frame_label):  
    frame.set(msg)  
    frame_label.update_idletasks()  
    if frame == filter_box:
        frame_label.after(2000, lambda: frame.set(""))
  
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
            update_status('Data successfully sent!', status_var, status_label)  
        else:  
            update_status('No serial port found!', status_var, status_label)  
    except Exception as e:  
        update_status('Error: ' + str(e), status_var, status_label)  

def lift_window():
    root.focus_force()                    # Focus the window

root = tk.Tk()
root.minsize(850, 650)
root.after(0, lift_window)  # Schedule it to run just after window starts
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title('Data Sender to STM32')
    
main_frame = ttk.Frame(root)  
main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW") 
main_frame.columnconfigure((0, 1), weight=1)  # Combine columnconfigure calls
main_frame.rowconfigure(0, weight=1) 
  
# Left and Right columns  
col_left = ttk.Frame(main_frame)  
col_left.grid(row=0, column=0, sticky='n')  
col_right = ttk.Frame(main_frame)  
col_right.grid(row=0, column=1, sticky='n', padx=20)  

col_left.columnconfigure(0, weight=1)
col_right.columnconfigure(0, weight=1)

# Sampling frequency
fs_entries = []
init_fs_values = ["1000"]
frame_fs = ttk.LabelFrame(col_left, text='Sampling frequency')
frame_fs.grid(row=0, column=0, padx=6, pady=6, sticky="NSEW")
for i in range(1):
    e = ttk.Entry(frame_fs, width=7)
    e.insert(0, init_fs_values[i])
    e.grid(row=0, column=i)
    fs_entries.append(e)

# Matrix S (pre-filled with 1)  
s_entries = []  
init_values_S = [
    ["1", "0", "0"],
    ["0", "1", "0"],
    ["0", "0", "1"],
    ["0", "0", "0"]
]
frame_s = ttk.LabelFrame(col_left, text='Matrix S')  
frame_s.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")  
for i in range(4):  
    row_entries = []  
    for j in range(3):  
        e = ttk.Entry(frame_s, width=5)  
        e.insert(0, init_values_S[i][j])  
        e.grid(row=i, column=j)  
        row_entries.append(e)  
    s_entries.append(row_entries)  
  
# Switch sw1  
sw1_vars = [tk.IntVar(value=1) for _ in range(3)]  
frame_sw1 = ttk.LabelFrame(col_left, text='Switch sw1')  
frame_sw1.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")  
for i in range(3): 
    cb = ttk.Checkbutton(frame_sw1, text='sw1_' + str(i+1), variable=sw1_vars[i])  
    cb.grid(row=0, column=i)  
  
# Setpoint x_sp  
xsp_entries = [] 
init_xsp_values = ["0", "0", "0"] 
frame_xsp = ttk.LabelFrame(col_left, text='Setpoint x_sp')  
frame_xsp.grid(row=2, column=0, padx=5, pady=5, sticky="NSEW")  
for i in range(3):  
    e = ttk.Entry(frame_xsp, width=7) 
    e.insert(0, init_xsp_values[i]) 
    e.grid(row=0, column=i)  
    xsp_entries.append(e)  
  
# PID Matrix (Rows: PID, Columns: Kp, Ki, Kd)  
pid_entries = []  
init_pid_values = [
    ["0.1", "0.001", "0."],
    ["0.1", "0.001", "0."],
    ["0.1", "0.001", "0."]
]
frame_pid = ttk.LabelFrame(col_left, text='PID Matrix')  
frame_pid.grid(row=3, column=0, padx=5, pady=5, sticky="NSEW")  
# Column headers  
ttk.Label(frame_pid, text='Kp').grid(row=0, column=1)  
ttk.Label(frame_pid, text='Ki').grid(row=0, column=2)  
ttk.Label(frame_pid, text='Kd').grid(row=0, column=3)  
for i in range(3):  
    row_entries = []  
    ttk.Label(frame_pid, text='PID ' + str(i+1)).grid(row=i+1, column=0)  
    for j in range(3):  
        e = ttk.Entry(frame_pid, width=7)  
        e.insert(0, init_pid_values[i][j])
        e.grid(row=i+1, column=j+1)  
        row_entries.append(e)  
    pid_entries.append(row_entries)  
  
# Filters (Fourth order)  

filtro_entries = []  
frame_filtri = ttk.LabelFrame(col_right, text='Fourth Order Filters')  
frame_filtri.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")  
filters_type = ['Anti-aliasing', 'Filter']
for filtro_idx,type in zip(range(2), filters_type):  
    subframe = ttk.LabelFrame(frame_filtri, text=(type if type == 'Anti-aliasing' else 'Filter '))  
    subframe.grid(row=filtro_idx, column=0, padx=2, pady=2, sticky='w')  
    # First stage 
    ttk.Label(subframe, text='First Stage:').grid(row=0, column=0, sticky='w')  
    first_stage_entries = []
    first_stage_init_values = ["0.004824343357716229", "0.009648686539896796", "0.004824343384506867", "1.048599576362613", "-0.2961403575616704"]
    second_stage_init_entries = ["1.0", "2.000000036385403", "0.9999999944467821", "1.3209134308194246", "-0.632738792885275"]
    for i in range(5):  
        e = ttk.Entry(subframe, width=4) 
        e.insert(0, first_stage_init_values[i] if type == 'Anti-aliasing' else "0") 
        e.grid(row=0, column=i+1)
        first_stage_entries.append(e)  
    # Second stage  
    ttk.Label(subframe, text='Second Stage:').grid(row=1, column=0, sticky='w')  
    second_stage_entries = []  
    for i in range(5):  
        e = ttk.Entry(subframe, width=4)  
        e.insert(0, second_stage_init_entries[i] if type == 'Anti-aliasing' else "0")
        e.grid(row=1, column=i+1)  
        second_stage_entries.append(e)  
    filtro_entries.append((first_stage_entries, second_stage_entries))  
    
    if type == 'Filter':
    # Only for the 'Filter' (idx == 1)
  
        mode_var = tk.StringVar(value='manual')

# Dictionary to store the script parameters
        script_params = {
            'fs': '1000',
            'f0': '100',
            'order': '4',
            'type': 'lowpass',
            'Q': ''
        }

        def open_script_window():
            win = tk.Toplevel(root)
            win.title("Filter Design Parameters")

            fs_var = tk.StringVar(value=script_params['fs'])
            f0_var = tk.StringVar(value=script_params['f0'])
            order_var = tk.StringVar(value=script_params['order'])
            type_var = tk.StringVar(value=script_params['type'])
            Q_var = tk.StringVar(value=script_params['Q'])

            ttk.Label(win, text="Sampling frequency:").grid(row=0, column=0, sticky='w')
            ttk.Entry(win, textvariable=fs_var).grid(row=0, column=1)

            ttk.Label(win, text="Cut-off frequency:").grid(row=1, column=0, sticky='w')
            ttk.Entry(win, textvariable=f0_var).grid(row=1, column=1)

            ttk.Label(win, text="Filter order:").grid(row=2, column=0, sticky='w')
            ttk.Entry(win, textvariable=order_var).grid(row=2, column=1)

            ttk.Label(win, text="Q factor (for notch filter):").grid(row=3, column=0, sticky='w')
            ttk.Entry(win, textvariable=Q_var).grid(row=3, column=1)

            ttk.Label(win, text="Filter type:").grid(row=4, column=0, sticky='w')
            type_menu = ttk.Combobox(win, textvariable=type_var, values=['lowpass', 'highpass', 'notch'], state='readonly')
            type_menu.grid(row=4, column=1)

            def compute_and_fill():
                try:
                    fs = float(fs_var.get())
                    f0 = float(f0_var.get())
                    order = int(order_var.get())
                    ftype = type_var.get()
                    Q_text = Q_var.get()
                    Q = float(Q_var.get()) if Q_text else None
                    if ftype == 'notch' and Q is None:
                        update_status("Error: Q factor is required for notch filter.", filter_box, filter_status_label)
                        return
            
            # Save the parameters to the script_params dictionary
                    script_params['fs'] = fs_var.get()
                    script_params['f0'] = f0_var.get()
                    script_params['order'] = order_var.get()
                    script_params['type'] = type_var.get()
                    script_params['Q'] = Q_var.get()

                    coefs = filter_design(fs=fs, f0=f0, order=order, type=ftype, Q=Q)
                    for e, val in zip(first_stage_entries + second_stage_entries, coefs):
                        e.config(state='normal')
                        e.delete(0, tk.END)
                        e.insert(0, f"{val:.6g}")
                        e.config(state='disabled')
                    win.destroy()
                except Exception as e:
                    update_status(f"Error: Invalid parameters:\n{e}", filter_box, filter_status_label)

            ttk.Button(win, text="Compute", command=compute_and_fill).grid(row=5, column=0, columnspan=2, pady=10)

        def update_mode():
            if mode_var.get() == 'manual':
                for e in first_stage_entries + second_stage_entries:
                    e.config(state='normal')
            elif mode_var.get() == 'script':
                open_script_window()

        cb_frame = ttk.Frame(subframe)
        cb_frame.grid(row=2, column=0, columnspan=6, sticky='w', pady=(5,0))
        
        # Radio buttons for seleting the mode for filter design
        ttk.Radiobutton(cb_frame, text='Manual', variable=mode_var, value='manual', command=update_mode).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(cb_frame, text='Script', variable=mode_var, value='script', command=update_mode).grid(row=0, column=1, padx=5)

  
# Switch sw2  
sw2_vars = [tk.IntVar(value=1) for _ in range(3)]  
frame_sw2 = ttk.LabelFrame(col_right, text='Switch sw2')  
frame_sw2.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")  
for i in range(3):  
    cb = ttk.Checkbutton(frame_sw2, text='sw2_' + str(i+1), variable=sw2_vars[i])  
    cb.grid(row=0, column=i)  
  
# Offset x_os  
xos_entries = []  
init_xos_values = ["0", "0", "0"]
frame_xos = ttk.LabelFrame(col_right, text='Offset x_os')  
frame_xos.grid(row=2, column=0, padx=5, pady=5, sticky="NSEW")  
for i in range(3):  
    e = ttk.Entry(frame_xos, width=7)  
    e.insert(0, init_xos_values[i])
    e.grid(row=0, column=i)  
    xos_entries.append(e)  
  
# Matrix D (pre-filled with 1)  
d_entries = []  
init_values_D = [
    ["1", "0", "0", "0"],
    ["0", "1", "0", "0"],
    ["0", "0", "1", "0"]
]
frame_d = ttk.LabelFrame(col_right, text='Matrix D')  
frame_d.grid(row=3, column=0, padx=5, pady=5, sticky="NSEW")  
for i in range(np.shape(init_values_D)[0]):  
    row_entries = []  
    for j in range(np.shape(init_values_D)[1]):  
        e = ttk.Entry(frame_d, width=5)  
        e.insert(0, init_values_D[i][j])  
        e.grid(row=i, column=j)  
        row_entries.append(e)  
    d_entries.append(row_entries)  

filter_box = tk.StringVar()  
filter_status_label = tk.Label(frame_filtri, textvariable=filter_box, bg='black', fg='white', relief='sunken', anchor='w', width=50, height=2)  
filter_status_label.grid(row=2, column=0, columnspan=1, pady=10, sticky="NSEW")

# Status box (white text)  
status_var = tk.StringVar()  
status_label = tk.Label(main_frame, textvariable=status_var, bg='black', fg='white', relief='sunken', anchor='w', width=50)  
status_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="NSEW")  
  
# Send button  
ttk.Button(main_frame, text='Send Data', command=invia_dati).grid(row=1, column=0, columnspan=2, pady=15)  
  
# Serial port detection at startup  
uart_port = find_uart_port()  
if uart_port:  
    update_status('Serial port found: ' + uart_port, status_var, status_label)  
else:  
    update_status('No serial port found!', status_var, status_label)  
  
root.mainloop()  