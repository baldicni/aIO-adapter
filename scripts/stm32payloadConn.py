import serial
import struct
import numpy as np

'''
Old functions

def find_uart_port():  
    available_ports = [port for port in os.listdir('/dev') if port.startswith('ttyUSB') or port.startswith('ttyACM') or port.startswith('tty.usbmodem')]  
    if available_ports:  
        return '/dev/' + available_ports[0]  
    else:  
        return None 


'''

class STM32PayloadConn:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None

    def create_sys_frame(self, dest_ip_addr, sw1, sw2, reset_bytes):

        frame_format = '<4B4B4B4B284B4B'

        # Insert the function to print in the gui the number of bytes of frame data

        # Empty bytes
        empty_bytes = [np.uint8(0) for i in range(284)]  # Placeholder for empty bytes, can be modified later

        # Reset bytes: 4 byte
        if reset_bytes is None:
            reset_bytes = [np.uint8(0), np.uint8(0), np.uint8(0), np.uint8(0)]  # Placeholder for reset bytes, can be modified later
        
        # Control vector: 4 byte
        ctrl = [np.uint8(0), np.uint8(0), np.uint8(0), np.uint8(0XA3)]  # Placeholder for control vector, can be modified later
        
        frame_data = struct.pack(frame_format, *dest_ip_addr, *sw1, *sw2, *reset_bytes, *empty_bytes, *ctrl)
        print("Sys frame data: ", frame_data)
        print("Sys frame data length: ", len(frame_data))
        return frame_data
    
    def create_config_frame(self, S, x_sp, PID1_values, PID2_values, PID3_values,
                            filter_values_flat1, filter_values_flat2, filter_values_flat3,
                            x_os, D):
        #frame_format = '<12f4B3f3f3f3f10f10f10f4B3f12f4B'
        # Dynamically build me_format based on DOF and NUM_OF_ADC
        DOF = 3
        NUM_OF_ADC = 4
        # S Matrix: NUM_OF_ADC * DOF floats
        # Setpoint: DOF floats
        # PID: DOF * 3 floats (Kp, Ki, Kd)
        # Filter: DOF * 10 floats (2x5 per DOF)
        # Offset: DOF floats
        # D Matrix: DOF * NUM_OF_ADC floats
        # Limits: DOF * 3 floats
        # Control: 4 bytes

        frame_format = f'<{NUM_OF_ADC * DOF}f{DOF}f{DOF * 3}f{DOF * 10}f{DOF}f{DOF * NUM_OF_ADC}f{DOF * 2}f4B'

        # Insert the function to print in the gui the number of bytes of frame data

        # Limits: 3x2 = 6 float
        limits = [np.float32(-10.0), np.float32(10.0),
                  np.float32(-10.0), np.float32(10.0),
                  np.float32(-10.0), np.float32(10.0)]

        # Control vector: 4 byte
        ctrl = [np.uint8(0), np.uint8(0), np.uint8(0), np.uint8(0XA1)]  # Placeholder for control vector, can be modified later
        
        frame_data = struct.pack(frame_format, *S, *x_sp, 
                                    *PID1_values, *PID2_values, *PID3_values, 
                                    *filter_values_flat1, *filter_values_flat2, *filter_values_flat3, 
                                    *x_os, *D, *limits, *ctrl)
        print("Frame data: ", frame_data)
        print("Frame data length: ", len(frame_data))
        return frame_data
    
    #SIGNAL SEND FRAME
    
    def create_sinusoidal_frame(self, amplitudes, frequencies, enables):
        frame = bytearray(304)  # Same size as other frames
        
        # Pack amplitudes (3x float32)
        for i, amp in enumerate(amplitudes):
            frame[i*4:(i+1)*4] = struct.pack('f', amp)
        
        # Pack frequencies (3x float32)
        for i, freq in enumerate(frequencies):
            frame[12 + i*4:12 + (i+1)*4] = struct.pack('f', freq)
        
        # Pack enables (3x uint8)
        for i, en in enumerate(enables):
            frame[24 + i] = en
        
        # Set frame type (0xA5)
        frame[-1] = 0xA5
        
        return frame
 
    def send(self, frame_data):
        if self.port is not None:
            if frame_data is not None:
                try:
                    ser = serial.Serial(self.port, self.baudrate, timeout=1)
                    ser.write(frame_data)
                except Exception as e:
                    print(f"Error sending data: {e}")
                else:
                    ser.close()
                    return True
                
        return False


        