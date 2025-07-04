import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import numpy as np
from scipy.signal import sos2zpk, iirfilter, tf2sos, iirnotch
import serial.tools.list_ports
from itertools import repeat

import stm32payloadConn

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
    ports = serial.tools.list_ports.comports()
    available_ports = [port.device for port in ports]
    if available_ports:
        return available_ports[0] # Return the first found port
    else:
        return None  

class gui_JAP:
    def __init__(self, DOF=3):
        self.root = tk.Tk()
        self.root.minsize(1200, 400)
        self.root.after(0, self.lift_window)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.title('Data Sender to STM32')

        #root.iconbitmap('gui_JAP.ico')
        script_dir = os.path.dirname(os.path.abspath(__file__))
        large_icon = tk.PhotoImage(file=os.path.join(script_dir, "gui_JAP_64.png"))
        small_icon = tk.PhotoImage(file=os.path.join(script_dir, "gui_JAP_24.png"))
        self.root.iconphoto(True, large_icon, small_icon)

            
        main_frame = ttk.Frame(self.root)  
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW") 
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)
        main_frame.rowconfigure(2, weight=0)

        self.DOF = DOF
        
        # Left and Right columns  
        col_left = ttk.Frame(main_frame)  
        col_left.grid(row=0, column=0, sticky='NSEW')
        col_left.columnconfigure(0, weight=1)  
        for i in range(6): 
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
            e = ttk.Entry(frame_fs, width=7, style='Flat.TEntry')  
            e.insert(0, init_fs_values[i])  
            e.state(['readonly']) 
            e.grid(row=0, column=i, padx=5, pady=5, sticky="EW")  
            fs_entries.append(e)  

        # Matrix S
        self.s_entries = []  
        init_values_S = [
            ["1", "0", "0"],
            ["0", "1", "0"],
            ["0", "0", "1"],
            ["0", "0", "0"]
        ]
        frame_s = ttk.LabelFrame(col_left, text='Matrix S')  
        frame_s.grid(row=1, column=0, padx=6, pady=3, sticky="NSEW")

        # Add column labels
        for j in range(self.DOF):
            frame_s.columnconfigure(j+1, weight=1)
            ttk.Label(frame_s, text=f'DOF {j+1}').grid(row=0, column=j+1, padx=2, pady=2, sticky="EW")

        # Add row labels and entries
        for i in range(4):  
            row_entries = []  
            ttk.Label(frame_s, text=f'ADC {i+1}').grid(row=i+1, column=0, padx=2, pady=2, sticky="EW")
            for j in range(3):  
                e = ttk.Entry(frame_s, width=5)  
                e.insert(0, init_values_S[i][j])  
                e.grid(row=i+1, column=j+1, padx=2, pady=2, sticky="EW")  # .
                row_entries.append(e)  
            self.s_entries.append(row_entries)  
        
        # Switch sw1  
        self.sw1_vars = [tk.IntVar(value=1) for _ in range(self.DOF)]  
        frame_sw1 = ttk.LabelFrame(col_left, text='Switch sw1')  
        frame_sw1.grid(row=2, column=0, padx=6, pady=3, sticky="NSEW")
        for j in range(4):  # Aumentato a 4 per il bottone di toggle
            frame_sw1.columnconfigure(j, weight=1)

        # Close loop 1
        self.sw1_toggle_var = tk.IntVar(value=1)  
        self.sw1_toggle_button = tk.Button(
            frame_sw1, 
            text="Close loop 1", 
            command=self.toggle_sw1_loop,
            relief=tk.SUNKEN,  
            bg='lightgreen'   
        )
        self.sw1_toggle_button.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        # Checkbox sw1  
        for i in range(self.DOF):  
            cb = ttk.Checkbutton(  
                frame_sw1,   
                text='sw1_' + str(i+1),   
                variable=self.sw1_vars[i],  
                command=lambda i=i: (self.sw1_vars[i].get(), self.send_system_data()) 
            )    
            cb.grid(row=0, column=i+1, padx=5, pady=5, sticky="EW") 
        
        # Setpoint x_sp  
        self.xsp_entries = [] 
        init_xsp_values = ["0", "0", "0"] 
        frame_xsp = ttk.LabelFrame(col_left, text='Setpoint x_sp')  
        frame_xsp.grid(row=3, column=0, padx=6, pady=3, sticky="NSEW")
        for j in range(3):
            frame_xsp.columnconfigure(j, weight=1)
        for i in range(3):  
            e = ttk.Entry(frame_xsp, width=7) 
            e.insert(0, init_xsp_values[i]) 
            e.grid(row=0, column=i, padx=2, pady=5, sticky="EW")  # .
            self.xsp_entries.append(e)  
        
        # PID Matrix
        self.pid_entries = []  
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
            self.pid_entries.append(row_entries)  

        # Reset PID button
        reset_pid_button = ttk.Button(frame_pid, text="Reset all PIDs", command= lambda: self.reset_pid(4))
        reset_pid_button.grid(row=6, column=1, columnspan=3, pady=5, sticky="EW")

        # Reset PID1 button
        reset_pid_button1 = ttk.Button(frame_pid, text="Reset PID1", command=lambda: self.reset_pid(1))
        reset_pid_button1.grid(row=5, column=1, columnspan=1, pady=5, sticky="EW")

        # Reset PID2 button
        reset_pid_button2 = ttk.Button(frame_pid, text="Reset PID2", command=lambda: self.reset_pid(2))
        reset_pid_button2.grid(row=5, column=2, columnspan=1, pady=5, sticky="EW")

        # Reset PID3 button
        reset_pid_button3 = ttk.Button(frame_pid, text="Reset PID3", command=lambda: self.reset_pid(3))
        reset_pid_button3.grid(row=5, column=3, columnspan=1, pady=5, sticky="EW")


        frame_antialiasing = ttk.LabelFrame(col_left, text='Anti-aliasing Filter')  
        frame_antialiasing.grid(row=5, column=0, padx=6, pady=3, sticky="NSEW")
        frame_antialiasing.columnconfigure(0, weight=0)  
        for j in range(1, 6):  # 5 colonne per i valori numerici
            frame_antialiasing.columnconfigure(j, weight=1)

        # First stage 
        ttk.Label(frame_antialiasing, text='First Stage:').grid(row=0, column=0, sticky='w', padx=2)  
        first_stage_entries = []
        first_stage_init_values = ["0.004824343357716229", "0.009648686539896796", "0.004824343384506867", "1.048599576362613", "-0.2961403575616704"]
        second_stage_init_entries = ["1.0", "2.000000036385403", "0.9999999944467821", "1.3209134308194246", "-0.632738792885275"]
        for i in range(5):  
            e = ttk.Entry(frame_antialiasing, width=4) 
            e.insert(0, first_stage_init_values[i]) 
            e.grid(row=0, column=i+1, padx=1, pady=1, sticky="EW")
            e.state(['readonly']) 
            first_stage_entries.append(e)  

        # Second stage  
        ttk.Label(frame_antialiasing, text='Second Stage:').grid(row=1, column=0, sticky='w', padx=2)  
        second_stage_entries = []  
        for i in range(5):  
            e = ttk.Entry(frame_antialiasing, width=4)  
            e.insert(0, second_stage_init_entries[i])
            e.grid(row=1, column=i+1, padx=1, pady=1, sticky="EW")
            e.state(['readonly']) 
            second_stage_entries.append(e)  

        # Filters (Fourth order)  
        self.filtro_entries = [[], [], [], []]  
        self.filtro_entries[0] = (first_stage_entries, second_stage_entries)

        frame_filtri = ttk.LabelFrame(col_right, text='Fourth Order Filters')  
        frame_filtri.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        frame_filtri.columnconfigure(0, weight=1) 
        filters_type = ['Filter DOF1', 'Filter DOF2', 'Filter DOF3']
        for filtro_idx, type in zip(range(1,4), filters_type):  
            subframe = ttk.LabelFrame(frame_filtri, text=type)  
            subframe.grid(row=filtro_idx-1, column=0, padx=2, pady=2, sticky='NSEW')
            subframe.columnconfigure(0, weight=0)  
            for j in range(1, 6):  # 5 colonne per i valori numerici
                subframe.columnconfigure(j, weight=1)
            
            # First stage 
            ttk.Label(subframe, text='First Stage:').grid(row=0, column=0, sticky='w', padx=2)  
            first_stage_entries = []
            first_stage_init_values = ["0.167179", "0.334359", "0.167179", "-0.328976", "-0.0645877"]
            second_stage_init_entries = ["1.0", "2.0", "1.0", "-0.45312", "-0.466326"]
            for i in range(5):  
                e = ttk.Entry(subframe, width=4) 
                e.insert(0,first_stage_init_values[i]) 
                e.grid(row=0, column=i+1, padx=1, pady=1, sticky="EW")  # .
                e.state(['readonly']) 
                first_stage_entries.append(e)  
            # Second stage  
            ttk.Label(subframe, text='Second Stage:').grid(row=1, column=0, sticky='w', padx=2)  
            second_stage_entries = []  
            for i in range(5):  
                e = ttk.Entry(subframe, width=4)  
                e.insert(0,second_stage_init_entries[i])
                e.grid(row=1, column=i+1, padx=1, pady=1, sticky="EW")  # .
                e.state(['readonly']) 
                second_stage_entries.append(e)  
            self.filtro_entries[filtro_idx].append((first_stage_entries, second_stage_entries))  

            if type.startswith('Filter DOF'):
                dof_index = int(type[-1])
                
                # Crea un'istanza per questo DOF
                dof_filter = DOF_Filter(dof_index, (first_stage_entries, second_stage_entries))
                
                # Frame for radio buttons and reset button
                cb_frame = ttk.Frame(subframe)
                cb_frame.grid(row=2, column=0, columnspan=6, sticky='w', pady=(5,0))
                
                # Radio buttons for selecting the mode for filter design
                ttk.Radiobutton(
                    cb_frame, text='Manual', variable=dof_filter.mode_var, 
                    value='manual', 
                    command=lambda df=dof_filter: df.update_mode(root=self.root)
                ).grid(row=0, column=0, padx=5)
                ttk.Radiobutton(
                    cb_frame, text='Script', variable=dof_filter.mode_var, 
                    value='script', 
                    command=lambda df=dof_filter: df.update_mode(root=self.root)
                ).grid(row=0, column=1, padx=5)
                
                # Reset button
                reset_filter_button = ttk.Button(
                    cb_frame, text=f"Reset Filter DOF{dof_filter.index}", 
                    command=lambda df=dof_filter: self.call_reset_filter_for(df)
                )
                reset_filter_button.grid(row=0, column=2, padx=5, pady=5, sticky="W")

        
        # Switch sw2  
        self.sw2_vars = [tk.IntVar(value=1) for _ in range(3)]  
        frame_sw2 = ttk.LabelFrame(col_right, text='Switch sw2')  
        frame_sw2.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")
        for j in range(4):  # Aumentato a 4 per il bottone di toggle
            frame_sw2.columnconfigure(j, weight=1)

        # Close loop 2 button
        self.sw2_toggle_var = tk.IntVar(value=1)  
        self.sw2_toggle_button = tk.Button(
            frame_sw2, 
            text="Close loop 2", 
            command=self.toggle_sw2_loop,
            relief=tk.SUNKEN, 
            bg='lightgreen'    
        )
        self.sw2_toggle_button.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        
        # Checkbox sw2  
        for i in range(self.DOF):
            cb = ttk.Checkbutton(  
                frame_sw2,   
                text='sw2_' + str(i+1),   
                variable=self.sw2_vars[i],  
                command=lambda i=i: (self.sw2_vars[i].get(), self.send_system_data())
            )    
            cb.grid(row=0, column=i+1, padx=5, pady=5, sticky="EW") 

        # Offset x_os  
        self.xos_entries = []  
        init_xos_values = ["0", "0", "0"]
        frame_xos = ttk.LabelFrame(col_right, text='Offset x_os')  
        frame_xos.grid(row=2, column=0, padx=5, pady=5, sticky="NSEW")
        for j in range(3):
            frame_xos.columnconfigure(j, weight=1)
        for i in range(3):  
            e = ttk.Entry(frame_xos, width=7)  
            e.insert(0, init_xos_values[i])
            e.grid(row=0, column=i, padx=2, pady=2, sticky="EW")  
            self.xos_entries.append(e)  
        
        # Matrix D (pre-filled with 1)  
        self.d_entries = []  
        '''init_values_D = [
            ["1", "0", "0", "0"],
            ["0", "1", "0", "0"],
            ["0", "0", "1", "0"]
        ]'''
        init_values_D =[
            ["1", "0", "0"],
            ["0", "1", "0"],
            ["0", "0", "1"],
            ["0", "0", "0"]
        ]
        frame_d = ttk.LabelFrame(col_right, text='Matrix D')  
        frame_d.grid(row=3, column=0, padx=5, pady=5, sticky="NSEW")

        # Add column labels
        for j in range(np.shape(init_values_D)[1]):
            frame_d.columnconfigure(j+1, weight=1)
            ttk.Label(frame_d, text=f'DOF {j+1}').grid(row=0, column=j+1, padx=2, pady=2, sticky="EW")

        # Add row labels and entries
        for i in range(np.shape(init_values_D)[0]):  
            row_entries = []  
            ttk.Label(frame_d, text=f'PWM {i+1}').grid(row=i+1, column=0, padx=2, pady=2, sticky="EW")
            for j in range(np.shape(init_values_D)[1]):  
                e = ttk.Entry(frame_d, width=5)  
                e.insert(0, init_values_D[i][j])  
                e.grid(row=i+1, column=j+1, padx=2, pady=2, sticky="EW")  
                row_entries.append(e)  
            self.d_entries.append(row_entries)  

        # Signal injection
        # Storage for signal parameters
        self.signal_ampl = list(repeat(0., DOF))
        self.signal_freq = list(repeat(1., DOF))
        self.signal_en = list(repeat(False, 4))

        # Status box (white text)  
        self.status_var = tk.StringVar()  
        self.status_label = tk.Label(main_frame, textvariable=self.status_var, bg='black', fg='white', relief='sunken', anchor='w', width=50)  
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="NSEW")  
        
        # Frame per contenere entrambi i bottoni
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=15, sticky="W")

        send_button = ttk.Button(button_frame, text='Config loops', command=self.send_config_data, width = 25)
        send_button.pack(side="left", padx=(0, 10))

        self.send_signal_btn = ttk.Button(button_frame, text="Send Signal", command=self.open_signal_window, style='Accent.TButton', width = 25)
        self.send_signal_btn.pack(side="left")


        # IP Address field
        self.ip_addr_var = tk.StringVar(value="192.168.11.15")
        frame_ip = ttk.LabelFrame(main_frame, text='Destination IP Address')
        frame_ip.grid(row=1, column=1, padx=6, pady=3, sticky="NSEW")
        frame_ip.columnconfigure(0, weight=1)
        frame_ip.columnconfigure(1, weight=1)
        frame_ip.columnconfigure(2, weight=0)

        ttk.Label(frame_ip, text="IP Address:").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        ip_entry = ttk.Entry(frame_ip, textvariable=self.ip_addr_var, width=18)
        ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="EW")  

        send_ip_button = ttk.Button(frame_ip, text='Update IP', command=self.send_system_data)
        send_ip_button.grid(row=0, column=2, padx=5, pady=5, sticky="E")

        self.root = self.root
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Serial port detection at startup  
        uart_port = find_uart_port()  
        if uart_port:  
            self.update_status('Serial port found: ' + uart_port, self.status_var, self.status_label)  
        else:  
            self.update_status('No serial port found!', self.status_var, self.status_label)

        self.stm32 = stm32payloadConn.STM32PayloadConn(uart_port)

        self.root.mainloop()
    
    def lift_window(self):
        self.root.focus_force()                    # Focus the window

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def build_config_frame_data(self):
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
        # S Matrix 4x3 = 12 float
        S = [np.float32(self.s_entries[i][j].get()) for i in range(4) for j in range(self.DOF)]
        # print("Sensing Matrix: ", S)

        # Setpoint x_sp: 3 float
        x_sp = [np.float32(self.xsp_entries[i].get()) for i in range(self.DOF)]
        # print("Setpoint: ", x_sp)

        # PID: 3 float per DOF (Kp, Ki, Kd)
        PID1_values = []
        PID2_values = []
        PID3_values = []
        for dof in range(self.DOF):
            Kp = np.float32(self.pid_entries[dof][0].get())
            Ki = np.float32(self.pid_entries[dof][1].get())
            Kd = np.float32(self.pid_entries[dof][2].get())
            if dof == 0:
                PID1_values.append(Kp)
                PID1_values.append(Ki)
                PID1_values.append(Kd)
            elif dof == 1:
                PID2_values.append(Kp)
                PID2_values.append(Ki)
                PID2_values.append(Kd)
            else:
                PID3_values.append(Kp)
                PID3_values.append(Ki)
                PID3_values.append(Kd)
        print("PID1 values: ", PID1_values)
        print("PID2 values: ", PID2_values)
        print("PID3 values: ", PID3_values)

        # Filters: 10 floats fot each DOF
        filtro_entries_filter_1 = self.filtro_entries[1]  # DOF1
        filtro_entries_filter_2 = self.filtro_entries[2]  # DOF2
        filtro_entries_filter_3 = self.filtro_entries[3]  # DOF3
        filter_values_flat1 = [np.float32(e.get()) for stage in filtro_entries_filter_1 for entry_list in stage for e in entry_list]
        filter_values_flat2 = [np.float32(e.get()) for stage in filtro_entries_filter_2 for entry_list in stage for e in entry_list]
        filter_values_flat3 = [np.float32(e.get()) for stage in filtro_entries_filter_3 for entry_list in stage for e in entry_list]

        def print_filter_coeffs(filter_num, values):
            print(f"First stage coefficients filter{filter_num}: {values[:5]}")
            print(f"Second stage coefficients filter{filter_num}: {values[5:]}")

        print_filter_coeffs(1, filter_values_flat1)
        print_filter_coeffs(2, filter_values_flat2)
        print_filter_coeffs(3, filter_values_flat3)
        # print("Filter values: ", filter_values_flat1)
        # print("Filter values: ", filter_values_flat2)
        # print("Filter values: ", filter_values_flat3)

        # Offset x_os: 3 float
        x_os = [np.float32(self.xos_entries[i].get()) for i in range(self.DOF)]
        # print("Offset: ", x_os)

        # D Matrix: 3x4 = 12 float
        #D = [np.float32(d_entries[i][j].get()) for i in range(4) for j in range(3)]
        D = [np.float32(self.d_entries[i][j].get()) for j in range(self.DOF) for i in range(4)]
        for dof in range(self.DOF):
            row = D[dof*4 : (dof+1)*4]
            print(f"DOF {dof+1}: {row}")

        # print("Matrix D: ", D)

        cfg_frame = self.stm32.create_config_frame(
            S=S, 
            x_sp=x_sp, 
            PID1_values=PID1_values, 
            PID2_values=PID2_values, 
            PID3_values=PID3_values, 
            filter_values_flat1=filter_values_flat1, 
            filter_values_flat2=filter_values_flat2, 
            filter_values_flat3=filter_values_flat3, 
            x_os=x_os, 
            D=D
        )
        return cfg_frame
    
    def build_system_frame_data(self, reset_bytes=None):
        ''' 
            - IP destination address: 4 byte
            - Switch1 sw1: 4 byte
            - Switch2 sw2: 4 byte
            - Future use bytes: 260 bytes
            - Reset bytes: 4 byte
            - Control vector: 4 byte

            '''
        # IP destination address
        # Convert string IP "192.168.33.34" to uint32 representation (big-endian)
        ip_str = self.ip_addr_var.get()
        try:
            ip_bytes = [int(x) for x in ip_str.split('.')]
            if len(ip_bytes) != 4 or not all(0 <= b <= 255 for b in ip_bytes):
                raise ValueError
        except Exception:
            self.update_status('Invalid IP address format!', self.status_var, self.status_label)
            ip_bytes = [192, 168, 33, 34]
        dest_ip_addr = [np.uint8(b) for b in ip_bytes]

        # Switch 1: 3 byte
        sw1 = [np.uint8(self.sw1_vars[i].get()) for i in range(self.DOF)]
        sw1.append(np.uint8(0))  # Add a zero to the end of the list
        # print("Switch 1: ", sw1)

        # Switch 2: 3 byte
        sw2 = [np.uint8(self.sw2_vars[i].get()) for i in range(self.DOF)]
        sw2.append(np.uint8(0))  # Add a zero to the end of the list
        # print("Switch 2: ", sw2)

        cfg_frame = self.stm32.create_sys_frame(
            dest_ip_addr=dest_ip_addr,
            sw1=sw1,
            sw2=sw2,
            reset_bytes=reset_bytes,
            sig_ampl = np.float32(self.signal_ampl),
            sig_freq = self.signal_freq,
            sig_en = np.uint8(self.signal_en)
        )
        return cfg_frame

    # Reset PID f
    def reset_pid(self, index):
        match index:
            case 1:
                reset_bytes = [np.uint8(0X01), np.uint8(0), np.uint8(0), np.uint8(0)]
            case 2:
                reset_bytes = [np.uint8(0X02), np.uint8(0), np.uint8(0), np.uint8(0)]
            case 3:
                reset_bytes = [np.uint8(0X04), np.uint8(0), np.uint8(0), np.uint8(0)]
            case 4:
                reset_bytes = [np.uint8(0X07), np.uint8(0), np.uint8(0), np.uint8(0)]
        
        frame_data = self.build_system_frame_data(reset_bytes)
        self.send_data(frame_data)

    def send_config_data(self):
        frame_data = self.build_config_frame_data()
        self.send_data(frame_data)

    def send_system_data(self):
        frame_data = self.build_system_frame_data()
        self.send_data(frame_data)

    def send_data(self, frame_data):
        if self.stm32.send(frame_data):
            if frame_data is not None:
                self.update_status(f'Data successfully sent!   Frame Length: {len(frame_data)} bytes', self.status_var, self.status_label)
            else:
                self.update_status('Error: Frame data not generated.', self.status_var, self.status_label)
        else:
            self.update_status('No serial port found!', self.status_var, self.status_label)
    
    def update_status(self, msg, frame, frame_label):  
        frame.set(msg)
        frame_label.update_idletasks()
    
    # Closed loop toggles
    def toggle_sw1_loop(self):
        current_state = self.sw1_toggle_var.get()
        new_state = 0 if current_state else 1
        self.sw1_toggle_var.set(new_state)
        
        # Set same values for sw1
        for i in range(self.DOF):
            self.sw1_vars[i].set(new_state)
        
        
        self.sw1_toggle_button.config(
            relief=tk.SUNKEN if new_state else tk.RAISED,
            bg='lightgreen' if new_state else 'lightgray'
        )

        self.send_system_data()  # Send the updated state of sw1 to the STM32

    def toggle_sw2_loop(self):
        current_state = self.sw2_toggle_var.get()
        new_state = 0 if current_state else 1
        self.sw2_toggle_var.set(new_state)
        
        
        for i in range(self.DOF):
            self.sw2_vars[i].set(new_state)
        
        
        self.sw2_toggle_button.config(
            relief=tk.SUNKEN if new_state else tk.RAISED,
            bg='lightgreen' if new_state else 'lightgray'
        )

        self.send_system_data()  # Send the updated state of sw2 to the STM32

    def call_reset_filter_for(self, df):
        reset_bytes = df.reset_filter()

        frame_data = self.build_system_frame_data(reset_bytes)
        self.send_data(frame_data)
    
    def open_signal_window(self):
        win = tk.Toplevel(self.root)
        win.title("Sinusoidal Signal Config")
        win.geometry("400x250")

        # DOF Selection
        ttk.Label(win, text="DOF:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.dof_var = tk.IntVar(value=0)
        for i in range(self.DOF):
            ttk.Radiobutton(win, text=f"DOF {i+1}", variable=self.dof_var, value=i, command=lambda: rad(self, self.dof_var.get())).grid(row=0, column=i+1)

        # Amplitude
        ttk.Label(win, text="Amplitude (-1.0 to 1.0):").grid(row=1, column=0, sticky="w")
        self.amp_entry = ttk.Entry(win)
        self.amp_entry.insert(0, self.signal_ampl[self.dof_var.get()])
        self.amp_entry.grid(row=1, column=1, columnspan=3, sticky="ew")

        # Frequency
        ttk.Label(win, text="Frequency (Hz):").grid(row=2, column=0, sticky="w")
        self.freq_entry = ttk.Entry(win)
        self.freq_entry.insert(0, self.signal_freq[self.dof_var.get()])
        self.freq_entry.grid(row=2, column=1, columnspan=3, sticky="ew")

        def rad(self, dof_var):
            self.amp_entry.delete(0, tk.END)
            self.amp_entry.insert(0, self.signal_ampl[dof_var])
            self.freq_entry.delete(0, tk.END)
            self.freq_entry.insert(0, self.signal_freq[dof_var])
            self.enable_var.set(self.signal_en[dof_var])  # Update enable checkbox based on selected DOF

        # Enable Checkbox
        self.enable_var = tk.IntVar()
        ttk.Checkbutton(win, text="Enable Signal", variable=self.enable_var).grid(row=3, column=0, columnspan=4)
        self.enable_var.set(self.signal_en[self.dof_var.get()])  # Update enable checkbox based on selected DOF

        # Send Button
        ttk.Button(win, text="Send", command=lambda: self.send_sinusoidal_from_window(win)).grid(row=4, column=1, pady=10)
    

    def send_sinusoidal_from_window(self, window):
        try:
            dof = self.dof_var.get()  # Convert to 0-based index
            amp = float(self.amp_entry.get())
            freq = float(self.freq_entry.get())
            enable = self.enable_var.get()

            # Validate inputs
            if not -1.0 <= amp <= 1.0:
                raise ValueError("Amplitude must be between -1.0 and 1.0")
            if not 0.1 <= freq <= 100.0:
                raise ValueError("Frequency must be between 0.1 and 100.0 Hz")
 
            # Set selected DOF
            self.signal_ampl[dof] = amp
            self.signal_freq[dof] = freq
            self.signal_en[dof] = enable

            # Send via STM32
            #frame = self.stm32.create_sinusoidal_frame(amplitudes, frequencies, enables)
            frame = self.build_system_frame_data(reset_bytes=None)
            #frame = self.stm32.create_sys_frame(dest_ip_addr, sw1, sw2, reset_bytes, self.signal_ampl, self.signal_freq, self.signal_en)
            self.send_data(frame)
            
            window.destroy()
            self.update_status(f"Sent: DOF{dof+1} | Amp: {amp} | Freq: {freq}Hz | {'ON' if enable else 'OFF'}",
                            self.status_var, self.status_label)

        except ValueError as e:
            messagebox.showerror("Error", str(e))



# Crea una classe per gestire ogni DOF separatamente
class DOF_Filter(gui_JAP):
    def __init__(self, index, entries):
        self.index = index
        self.entries = entries
        self.mode_var = tk.StringVar(value='manual')
        self.script_params = {
            'fs': '1000',
            'f0': '100',
            'order': '4',
            'type': 'lowpass',
            'Q': ''
        }
    
    def open_script_window(self, root):
        win = tk.Toplevel(root)
        win.title(f"Filter Design Parameters - DOF {self.index}")

        fs_var = tk.StringVar(value=self.script_params['fs'])
        f0_var = tk.StringVar(value=self.script_params['f0'])
        order_var = tk.StringVar(value=self.script_params['order'])
        type_var = tk.StringVar(value=self.script_params['type'])
        Q_var = tk.StringVar(value=self.script_params['Q'])

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
                    self.update_status("Error: Q factor is required for notch filter.", self.status_var, self.status_label)
                    return
            
                # Salva i parametri
                self.script_params = {
                    'fs': fs_var.get(),
                    'f0': f0_var.get(),
                    'order': order_var.get(),
                    'type': type_var.get(),
                    'Q': Q_var.get()
                }

                coefs = filter_design(fs=fs, f0=f0, order=order, type=ftype, Q=Q)
                if ftype == 'notch':
                    coefs = np.concatenate((coefs, coefs))

                for e, val in zip(self.entries[0] + self.entries[1], coefs):
                    e.config(state='normal')
                    e.delete(0, tk.END)
                    e.insert(0, f"{val:.6g}")
                    e.config(state='disabled')
                win.destroy()
            except Exception as e:
                self.update_status(f"Error: Invalid parameters:\n{e}", self.status_var, self.status_label)

        ttk.Button(win, text="Compute", command=compute_and_fill).grid(row=5, column=0, columnspan=2, pady=10)
    
    def update_mode(self, root):
        if self.mode_var.get() == 'manual':
            for e in self.entries[0] + self.entries[1]:
                e.config(state='normal')
        elif self.mode_var.get() == 'script':
            self.open_script_window(root)
    
    def reset_filter(self):
        match self.index:
            case 1:
                reset_bytes = [np.uint8(0), np.uint8(0X10), np.uint8(0), np.uint8(0)]
            case 2:
                reset_bytes = [np.uint8(0), np.uint8(0X20), np.uint8(0), np.uint8(0)]
            case 3:
                reset_bytes = [np.uint8(0), np.uint8(0X40), np.uint8(0), np.uint8(0)]
        
        return reset_bytes
        #frame_data = self.build_system_frame_data(reset_bytes)
        #self.send_data(frame_data)

if __name__ == "__main__":
    gui_JAP()
