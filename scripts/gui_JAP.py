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

def build_frame_data():
    ''' 
        - Sensing Matrix: 4x3 = 12 floats concatenated rows 
        - Switch1 sw1: 3 bytes
        - Setpoint x_sp: 3 floats
        - PID 3 Vectors 3fx3 = 9 floats
        - Filter before PID: 2x5fx3 floats = 30 floats
        - Switch2 sw2: 3 bytes
        - Offset x_os: 3 floats
        - Matrix D: 3x4 = 12 floats concatenated rows

        '''
    if True:
        # S Matrix 4x3 = 12 float
        S = [np.float32(s_entries[i][j].get()) for j in range(3) for i in range(4)]
        # print("Sensing Matrix: ", S)

        # Switch 1: 3 byte
        sw1 = [np.int8(sw1_vars[i].get()) for i in range(3)]
        # print("Switch 1: ", sw1)

        # Setpoint x_sp: 3 float
        x_sp = [np.float32(xsp_entries[i].get()) for i in range(3)]
        # print("Setpoint: ", x_sp)

        # PID: 3 float per DOF (Kp, Ki, Kd)
        PID1_values = []
        PID2_values = []
        PID3_values = []
        for dof in range(3):
            Kp = np.float32(pid_entries[dof][0].get())
            Ki = np.float32(pid_entries[dof][1].get())
            Kd = np.float32(pid_entries[dof][2].get())
            PID1_values.append(Kp)
            PID2_values.append(Ki)
            PID3_values.append(Kd)
        # print("PID values: ", PID1_values)
        # print("PID values: ", PID2_values)
        # print("PID values: ", PID3_values)

        # Filters: 10 floats fot each DOF
        filtro_idx = 1  # Solo 'Filter'
        filtro_entries_filter_1 = filtro_entries[filtro_idx]
        filtro_entries_filter_2 = filtro_entries[filtro_idx]
        filtro_entries_filter_3 = filtro_entries[filtro_idx]
        filter_values_flat1 = [np.float32(e.get()) for stage in filtro_entries_filter_1 for e in stage]  # 10 valori
        filter_values_flat2 = [np.float32(e.get()) for stage in filtro_entries_filter_2 for e in stage]  # 10 valori
        filter_values_flat3 = [np.float32(e.get()) for stage in filtro_entries_filter_3 for e in stage]  # 10 valori
        # print("Filter values: ", filter_values_flat1)
        # print("Filter values: ", filter_values_flat2)
        # print("Filter values: ", filter_values_flat3)

        # Switch 2: 3 byte
        sw2 = [np.int8(sw2_vars[i].get()) for i in range(3)]
        # print("Switch 2: ", sw2)

        # Offset x_os: 3 float
        x_os = [np.float32(xos_entries[i].get()) for i in range(3)]
        # print("Offset: ", x_os)

        # D Matrix: 3x4 = 12 float
        D = [np.float32(d_entries[i][j].get()) for i in range(3) for j in range(4)]
        # print("Matrix D: ", D)

        frame_format = '<12f3B3f3f3f3f10f10f10f3B3f12f'

        # Insert the function to print in the gui the number of bytes of frame data
        
        frame_data = struct.pack(frame_format, *S, *sw1, *x_sp, 
                                 *PID1_values, *PID2_values, *PID3_values, 
                                 *filter_values_flat1, *filter_values_flat2, *filter_values_flat3, 
                                 *sw2, *x_os, *D)
        print("Frame data: ", frame_data)
        print("Frame data length: ", len(frame_data))
        return frame_data
    
def invia_dati():  

    frame_data = build_frame_data()

    if uart_port:
        if frame_data is not None:
            ser = serial.Serial(uart_port, 115200, timeout=1)
            ser.write(frame_data)
            ser.close()
            update_status(f'Data successfully sent!   Frame Length: {len(frame_data)} bytes', status_var, status_label)
        else:
            update_status('Error: Frame data not generated.', status_var, status_label)
    else:
        update_status('No serial port found!', status_var, status_label)

def lift_window():
    root.focus_force()                    # Focus the window


# Closed loop toggles
def toggle_sw1_loop():
    current_state = sw1_toggle_var.get()
    new_state = 0 if current_state else 1
    sw1_toggle_var.set(new_state)
    
    # Set same values for sw1
    for i in range(3):
        sw1_vars[i].set(new_state)
    
    
    sw1_toggle_button.config(
        relief=tk.SUNKEN if new_state else tk.RAISED,
        bg='lightgreen' if new_state else 'lightgray'
    )

def toggle_sw2_loop():
    current_state = sw2_toggle_var.get()
    new_state = 0 if current_state else 1
    sw2_toggle_var.set(new_state)
    
    
    for i in range(3):
        sw2_vars[i].set(new_state)
    
    
    sw2_toggle_button.config(
        relief=tk.SUNKEN if new_state else tk.RAISED,
        bg='lightgreen' if new_state else 'lightgray'
    )


root = tk.Tk()
root.minsize(850, 650)
root.after(0, lift_window)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title('Data Sender to STM32')
    
main_frame = ttk.Frame(root)  
main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW") 
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=0)
main_frame.rowconfigure(2, weight=0)
  
# Left and Right columns  
col_left = ttk.Frame(main_frame)  
col_left.grid(row=0, column=0, sticky='NSEW')
col_left.columnconfigure(0, weight=1)  
for i in range(5): 
    col_left.rowconfigure(i, weight=0)

col_right = ttk.Frame(main_frame)  
col_right.grid(row=0, column=1, sticky='NSEW', padx=20)  
col_right.columnconfigure(0, weight=1)  
for i in range(4):  
    col_right.rowconfigure(i, weight=0)

# Sampling frequency
fs_entries = []
init_fs_values = ["1000"]
frame_fs = ttk.LabelFrame(col_left, text='Sampling frequency')
frame_fs.grid(row=0, column=0, padx=6, pady=(6, 3), sticky="NSEW")
frame_fs.columnconfigure(0, weight=1)  
for i in range(1):
    e = ttk.Entry(frame_fs, width=7)
    e.insert(0, init_fs_values[i])
    e.grid(row=0, column=i, padx=5, pady=5, sticky="EW")  
    fs_entries.append(e)

# Matrix S
s_entries = []  
init_values_S = [
    ["1", "0", "0"],
    ["0", "1", "0"],
    ["0", "0", "1"],
    ["0", "0", "0"]
]
frame_s = ttk.LabelFrame(col_left, text='Matrix S')  
frame_s.grid(row=1, column=0, padx=6, pady=3, sticky="NSEW")

for j in range(3):
    frame_s.columnconfigure(j, weight=1)
for i in range(4):  
    row_entries = []  
    for j in range(3):  
        e = ttk.Entry(frame_s, width=5)  
        e.insert(0, init_values_S[i][j])  
        e.grid(row=i, column=j, padx=2, pady=2, sticky="EW")  # .
        row_entries.append(e)  
    s_entries.append(row_entries)  
  
# Switch sw1  
sw1_vars = [tk.IntVar(value=1) for _ in range(3)]  
frame_sw1 = ttk.LabelFrame(col_left, text='Switch sw1')  
frame_sw1.grid(row=2, column=0, padx=6, pady=3, sticky="NSEW")
for j in range(4):  # Aumentato a 4 per il bottone di toggle
    frame_sw1.columnconfigure(j, weight=1)

# Close loop 1
sw1_toggle_var = tk.IntVar(value=1)  
sw1_toggle_button = tk.Button(
    frame_sw1, 
    text="Close loop 1", 
    command=toggle_sw1_loop,
    relief=tk.SUNKEN,  
    bg='lightgreen'   
)
sw1_toggle_button.grid(row=0, column=0, padx=5, pady=5, sticky="W")

# Checkbox sw1
for i in range(3):
    cb = ttk.Checkbutton(frame_sw1, text='sw1_' + str(i+1), variable=sw1_vars[i])  
    cb.grid(row=0, column=i+1, padx=5, pady=5, sticky="EW")
  
# Setpoint x_sp  
xsp_entries = [] 
init_xsp_values = ["0", "0", "0"] 
frame_xsp = ttk.LabelFrame(col_left, text='Setpoint x_sp')  
frame_xsp.grid(row=3, column=0, padx=6, pady=3, sticky="NSEW")
for j in range(3):
    frame_xsp.columnconfigure(j, weight=1)
for i in range(3):  
    e = ttk.Entry(frame_xsp, width=7) 
    e.insert(0, init_xsp_values[i]) 
    e.grid(row=0, column=i, padx=2, pady=5, sticky="EW")  # .
    xsp_entries.append(e)  
  
# PID Matrix
pid_entries = []  
init_pid_values = [
    ["0.1", "0.001", "0."],
    ["0.1", "0.001", "0."],
    ["0.1", "0.001", "0."]
]
frame_pid = ttk.LabelFrame(col_left, text='PID Matrix')  
frame_pid.grid(row=4, column=0, padx=6, pady=3, sticky="NSEW")

for j in range(4): 
    frame_pid.columnconfigure(j, weight=1)
# Column headers  
ttk.Label(frame_pid, text='Kp').grid(row=0, column=1, padx=2, pady=2)  
ttk.Label(frame_pid, text='Ki').grid(row=0, column=2, padx=2, pady=2)  
ttk.Label(frame_pid, text='Kd').grid(row=0, column=3, padx=2, pady=2)  
for i in range(3):  
    row_entries = []  
    ttk.Label(frame_pid, text='PID ' + str(i+1)).grid(row=i+1, column=0, padx=2, pady=2)  
    for j in range(3):  
        e = ttk.Entry(frame_pid, width=7)  
        e.insert(0, init_pid_values[i][j])
        e.grid(row=i+1, column=j+1, padx=2, pady=2, sticky="EW")  # .
        row_entries.append(e)  
    pid_entries.append(row_entries)  

# Reset PID f
def reset_pid():
    return True

# Reset PID button
reset_pid_button = ttk.Button(frame_pid, text="Reset PID", command=reset_pid)
reset_pid_button.grid(row=4, column=0, columnspan=4, pady=5, sticky="EW")
  
# Filters (Fourth order)  
filtro_entries = []  
frame_filtri = ttk.LabelFrame(col_right, text='Fourth Order Filters')  
frame_filtri.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
frame_filtri.columnconfigure(0, weight=1) 
filters_type = ['Anti-aliasing', 'Filter']
for filtro_idx, type in zip(range(2), filters_type):  
    subframe = ttk.LabelFrame(frame_filtri, text=(type if type == 'Anti-aliasing' else 'Filter '))  
    subframe.grid(row=filtro_idx, column=0, padx=2, pady=2, sticky='NSEW')
    subframe.columnconfigure(0, weight=0)  
    for j in range(1, 6):  # 5 colonne per i valori numerici
        subframe.columnconfigure(j, weight=1)
    
    # First stage 
    ttk.Label(subframe, text='First Stage:').grid(row=0, column=0, sticky='w', padx=2)  
    first_stage_entries = []
    first_stage_init_values = ["0.004824343357716229", "0.009648686539896796", "0.004824343384506867", "1.048599576362613", "-0.2961403575616704"]
    second_stage_init_entries = ["1.0", "2.000000036385403", "0.9999999944467821", "1.3209134308194246", "-0.632738792885275"]
    for i in range(5):  
        e = ttk.Entry(subframe, width=4) 
        e.insert(0, first_stage_init_values[i] if type == 'Anti-aliasing' else "0") 
        e.grid(row=0, column=i+1, padx=1, pady=1, sticky="EW")  # .
        first_stage_entries.append(e)  
    # Second stage  
    ttk.Label(subframe, text='Second Stage:').grid(row=1, column=0, sticky='w', padx=2)  
    second_stage_entries = []  
    for i in range(5):  
        e = ttk.Entry(subframe, width=4)  
        e.insert(0, second_stage_init_entries[i] if type == 'Anti-aliasing' else "0")
        e.grid(row=1, column=i+1, padx=1, pady=1, sticky="EW")  # .
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

            win.columnconfigure(0, weight=0)
            win.columnconfigure(1, weight=1)

            ttk.Label(win, text="Sampling frequency:").grid(row=0, column=0, sticky='w', padx=5, pady=3)
            ttk.Entry(win, textvariable=fs_var).grid(row=0, column=1, sticky="EW", padx=5, pady=3)

            ttk.Label(win, text="Cut-off frequency:").grid(row=1, column=0, sticky='w', padx=5, pady=3)
            ttk.Entry(win, textvariable=f0_var).grid(row=1, column=1, sticky="EW", padx=5, pady=3)

            ttk.Label(win, text="Filter order:").grid(row=2, column=0, sticky='w', padx=5, pady=3)
            ttk.Entry(win, textvariable=order_var).grid(row=2, column=1, sticky="EW", padx=5, pady=3)

            ttk.Label(win, text="Q factor (for notch filter):").grid(row=3, column=0, sticky='w', padx=5, pady=3)
            ttk.Entry(win, textvariable=Q_var).grid(row=3, column=1, sticky="EW", padx=5, pady=3)

            ttk.Label(win, text="Filter type:").grid(row=4, column=0, sticky='w', padx=5, pady=3)
            type_menu = ttk.Combobox(win, textvariable=type_var, values=['lowpass', 'highpass', 'notch'], state='readonly')
            type_menu.grid(row=4, column=1, sticky="EW", padx=5, pady=3)

            def compute_and_fill():
                try:
                    fs = np.float32(fs_var.get())
                    f0 = np.float32(f0_var.get())
                    order = np.int8(order_var.get())
                    ftype = type_var.get()
                    Q_text = Q_var.get()
                    Q = np.float32(Q_var.get()) if Q_text else None
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

        # Reset filters f
        def reset_filter():
           return True
        
        # Frame for radio buttons and reset button
        cb_frame = ttk.Frame(subframe)
        cb_frame.grid(row=2, column=0, columnspan=6, sticky='w', pady=(5,0))
        
        # Radio buttons for seleting the mode for filter design
        ttk.Radiobutton(cb_frame, text='Manual', variable=mode_var, value='manual', command=update_mode).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(cb_frame, text='Script', variable=mode_var, value='script', command=update_mode).grid(row=0, column=1, padx=5)
        
        # Reset button
        reset_filter_button = ttk.Button(cb_frame, text="Reset Filter", command=reset_filter)
        reset_filter_button.grid(row=0, column=2, padx=5, pady=5, sticky="W")

  
# Switch sw2  
sw2_vars = [tk.IntVar(value=1) for _ in range(3)]  
frame_sw2 = ttk.LabelFrame(col_right, text='Switch sw2')  
frame_sw2.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")
for j in range(4):  # Aumentato a 4 per il bottone di toggle
    frame_sw2.columnconfigure(j, weight=1)

# Close loop 2 button
sw2_toggle_var = tk.IntVar(value=1)  
sw2_toggle_button = tk.Button(
    frame_sw2, 
    text="Close loop 2", 
    command=toggle_sw2_loop,
    relief=tk.SUNKEN, 
    bg='lightgreen'    
)
sw2_toggle_button.grid(row=0, column=0, padx=5, pady=5, sticky="W")

# Checkbox sw2
for i in range(3):  
    cb = ttk.Checkbutton(frame_sw2, text='sw2_' + str(i+1), variable=sw2_vars[i])  
    cb.grid(row=0, column=i+1, padx=5, pady=5, sticky="EW")
  
# Offset x_os  
xos_entries = []  
init_xos_values = ["0", "0", "0"]
frame_xos = ttk.LabelFrame(col_right, text='Offset x_os')  
frame_xos.grid(row=2, column=0, padx=5, pady=5, sticky="NSEW")
for j in range(3):
    frame_xos.columnconfigure(j, weight=1)
for i in range(3):  
    e = ttk.Entry(frame_xos, width=7)  
    e.insert(0, init_xos_values[i])
    e.grid(row=0, column=i, padx=2, pady=2, sticky="EW")  
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

for j in range(4):
    frame_d.columnconfigure(j, weight=1)
for i in range(np.shape(init_values_D)[0]):  
    row_entries = []  
    for j in range(np.shape(init_values_D)[1]):  
        e = ttk.Entry(frame_d, width=5)  
        e.insert(0, init_values_D[i][j])  
        e.grid(row=i, column=j, padx=2, pady=2, sticky="EW")  
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
send_button = ttk.Button(main_frame, text='Send Data', command=invia_dati)
send_button.grid(row=1, column=0, columnspan=2, pady=15)
  
# Serial port detection at startup  
uart_port = find_uart_port()  
if uart_port:  
    update_status('Serial port found: ' + uart_port, status_var, status_label)  
else:  
    update_status('No serial port found!', status_var, status_label)  

  
root.mainloop()