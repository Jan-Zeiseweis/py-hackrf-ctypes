from functools import wraps

from ctypes import (
    CDLL,
    CFUNCTYPE,
    POINTER,
    Structure,
    c_byte,
    c_ubyte,
    c_char,
    c_double,
    c_int,
    c_uint ,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
    c_ulong,
    c_void_p,
    cast,
)

class hackrf_device(Structure):
    pass

P_hackrf_device = POINTER(hackrf_device)

class hackrf_transfer(Structure):
    _fields_ = [
        ("hackrf_device", P_hackrf_device),
        ("buffer", POINTER(c_byte)),
        ("buffer_length", c_int),
        ("valid_length", c_int),
        ("rx_ctx", c_void_p),
        ("tx_ctx", c_void_p)
    ]

P_hackrf_transfer = POINTER(hackrf_transfer)

_callback = CFUNCTYPE(c_int, P_hackrf_transfer)

hackrf_device._fields_ = [
    ("usb_device", POINTER(c_void_p)),
    ("transfers", POINTER(P_hackrf_transfer)),
    ("callback", _callback),
    ("transfer_thread_started", c_int),
    ("transfer_thread", c_ulong),
    ("transfer_count", c_uint32),
    ("buffer_size", c_uint32),
    ("streaming", c_int),
    ("rx_ctx", c_void_p),
    ("tx_ctx", c_void_p)
]

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def prepare_libhackrf(libhackrf):
    libhackrf.hackrf_open.argtypes = [POINTER(P_hackrf_device)]
    libhackrf.hackrf_close.argtypes = [P_hackrf_device]
    libhackrf.hackrf_start_rx.argtypes = [P_hackrf_device, _callback, c_void_p]
    libhackrf.hackrf_stop_rx.argtypes = [P_hackrf_device]
    libhackrf.hackrf_start_tx.argtypes = [P_hackrf_device, _callback, c_void_p]
    libhackrf.hackrf_stop_tx.argtypes = [P_hackrf_device]
    libhackrf.hackrf_is_streaming.argtypes = [P_hackrf_device]
    libhackrf.hackrf_max2837_read.argtypes = [P_hackrf_device, c_uint8, POINTER(c_uint16)]
    libhackrf.hackrf_max2837_write.argtypes = [P_hackrf_device, c_uint8, c_uint16]
    libhackrf.hackrf_si5351c_read.argtypes = [P_hackrf_device, c_uint16, POINTER(c_uint16)]
    libhackrf.hackrf_si5351c_write.argtypes = [P_hackrf_device, c_uint16, c_uint16]
    libhackrf.hackrf_set_baseband_filter_bandwidth.argtypes = [P_hackrf_device, c_uint32]
    libhackrf.hackrf_rffc5071_read.argtypes = [P_hackrf_device, c_uint8, POINTER(c_uint16)]
    libhackrf.hackrf_rffc5071_write.argtypes = [P_hackrf_device, c_uint8, c_uint16]
    libhackrf.hackrf_spiflash_erase.argtypes = [P_hackrf_device]
    libhackrf.hackrf_spiflash_write.argtypes = [P_hackrf_device, c_uint32, c_uint16, POINTER(c_ubyte)]
    libhackrf.hackrf_spiflash_read.argtypes = [P_hackrf_device, c_uint32, c_uint16, POINTER(c_ubyte)]
    libhackrf.hackrf_cpld_write.argtypes = [P_hackrf_device, POINTER(c_ubyte), c_uint]
    libhackrf.hackrf_board_id_read.argtypes = [P_hackrf_device, POINTER(c_uint8)]
    libhackrf.hackrf_version_string_read.argtypes = [P_hackrf_device, POINTER(c_char), c_uint8]
    libhackrf.hackrf_set_freq.argtypes = [P_hackrf_device, c_uint64]
    libhackrf.hackrf_set_sample_rate_manual.argtypes = [P_hackrf_device, c_uint32, c_uint32]
    libhackrf.hackrf_set_sample_rate.argtypes = [P_hackrf_device, c_double]
    libhackrf.hackrf_set_amp_enable.argtypes = [P_hackrf_device, c_uint8]
    libhackrf.hackrf_board_partid_serialno_read.argtypes = [P_hackrf_device]
    libhackrf.hackrf_set_lna_gain.argtypes = [P_hackrf_device, c_uint32]
    libhackrf.hackrf_set_vga_gain.argtypes = [P_hackrf_device, c_uint32]
    libhackrf.hackrf_set_txvga_gain.argtypes = [P_hackrf_device, c_uint32]
    libhackrf.hackrf_set_antenna_enable.argtypes = [P_hackrf_device, c_uint8]
    libhackrf.hackrf_compute_baseband_filter_bw_round_down_lt.restype = c_uint32
    libhackrf.hackrf_compute_baseband_filter_bw_round_down_lt.argtypes = [c_uint32]
    libhackrf.hackrf_compute_baseband_filter_bw.restype = c_uint32
    libhackrf.hackrf_compute_baseband_filter_bw.argtypes = [c_uint32]



def opened(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_open:
            raise BaseException("Device not opened")
        else:
            return func(self, *args, **kwargs)
    return wrapper

