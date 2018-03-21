import os
import logging
import numpy as np

from functools import partial
from constants import HackRfError
from helpers import prepare_libhackrf, opened, P_hackrf_device, _callback

logging.basicConfig()
logger = logging.getLogger('HackRf')
logger.setLevel(logging.DEBUG)

from ctypes import CDLL, c_byte, cast, POINTER

libhackrf = CDLL('/opt/local/lib/libhackrf.dylib')

class HackRf(object):

    def __init__(self):
        prepare_libhackrf(libhackrf)
        self.device = P_hackrf_device()
        self.callback = None
        self.is_open = False

    def __del__(self):
        if self.is_open == True:
            self.exit()

    def setup(self):
        libhackrf.hackrf_init()
        return self.open()

    def exit(self):
        ret = self.close()
        libhackrf.hackrf_exit()
        return ret

    def open(self):
        self.is_open = libhackrf.hackrf_open(self.device) == HackRfError.HACKRF_SUCCESS
        if not self.is_open:
            logger.error('No Hack Rf Detected!')
            return self.is_open

        logger.debug('Successfully open HackRf device')
        return self.is_open

    @opened
    def close(self):
        ret = libhackrf.hackrf_close(self.device)
        if ret == HackRfError.HACKRF_SUCCESS:
            self.is_open = False
            logger.debug('Successfully close HackRf device')
            return True
        else:
            logger.error('Failed to close!')

    @opened
    def start_rx_mode(self, set_callback):
        self.callback = _callback(set_callback)
        ret = libhackrf.hackrf_start_rx(self.device, self.callback, None)
        if ret == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully start HackRf in Recieve Mode')
            return True
        else:
            logger.error('Failed to start HackRf in Recieve Mode')

    @opened
    def stop_rx_mode(self):
        ret = libhackrf.hackrf_stop_rx(self.device)
        if ret == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully stop HackRf in Recieve Mode')
            return True
        else:
            logger.error('Failed to stop HackRf in Recieve Mode')
        return ret

    @opened
    def start_tx_mode(self, set_callback):
        self.callback = _callback(set_callback)
        ret =  libhackrf.hackrf_start_tx(self.device, self.callback, None)
        if ret == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully start HackRf in Transfer Mode')
            return True
        else:
            logger.error('Failed to start HackRf in Transfer Mode')

    @opened
    def stop_tx_mode(self):
        ret = libhackrf.hackrf_stop_tx(self.device)
        if ret == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully stop HackRf in Transfer Mode')
            return True
        else:
            logger.error('Failed to stop HackRf in Transfer Mode')

    @opened
    def board_id_read(self):
        value = c_uint8()
        ret = libhackrf.hackrf_board_id_read(self.device, byref(value))
        if ret == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully got Board Id')
            return value.value
        else:
            logger.error('Failed to get Board Id')

    @opened
    def version_string_read(self):
        version = create_string_buffer(20)
        lenth = c_uint8(20)
        ret = libhackrf.hackrf_version_string_read(self.device, version, lenth)
        if ret == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully got HackRf Version String')
            return version.value
        else:
            logger.error('Failed to get Version String')

    @opened
    def set_freq(self, freq_hz):
        ret = libhackrf.hackrf_set_freq(self.device, freq_hz)
        if ret == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully set frequency with value [%d]', freq_hz)
            return True
        else:
            logger.error('Error setting frequency with value [%d]', freq_hz)

    @opened
    def is_streaming(self):
        ret = libhackrf.hackrf_is_streaming(self.device)
        if(ret == 1):
            return True
        else:
            return False

    @opened
    def set_lna_gain(self, value):
        ''' Sets the LNA gain, in 8Db steps, maximum value of 40 '''
        result = libhackrf.hackrf_set_lna_gain(self.device, value)
        if result == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully set LNA gain to [%d]', value)
            return True
        else:
            logger.error('Failed to set LNA gain to [%d]', value)

    @opened
    def set_vga_gain(self, value):
        ''' Sets the vga gain, in 2db steps, maximum value of 62 '''
        result = libhackrf.hackrf_set_vga_gain(self.device, value)
        if result == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully set VGA gain to [%d]', value)
            return True
        else:
            logger.error('Failed to set VGA gain to [%d]', value)

    @opened
    def set_txvga_gain(self, value):
        ''' Sets the txvga gain, in 1db steps, maximum value of 47 '''
        result = libhackrf.hackrf_set_txvga_gain(self.device, value)
        if result == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully set TXVGA gain to [%d]', value)
            return True
        else:
            logger.error('Failed to set TXVGA gain to [%d]', value)


    @opened
    def set_antenna_enable(self, value):
        if value == True:
            val = 1
        else:
            val = 0
        result =  libhackrf.hackrf_set_antenna_enable(self.device, val)
        if result == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully set antenna_enable')
            return True
        else:
            logger.error('Failed to set antenna_enable')

    @opened
    def set_sample_rate(self, freq):
        result = libhackrf.hackrf_set_sample_rate(self.device, freq)
        if result != HackRfError.HACKRF_SUCCESS:
            logger.error('Error setting Sample Rate with Frequency [%d]', freq)
        else:
            logger.debug(
                'Successfully set Sample Rate with Frequency [%d]', freq)
            return True

    @opened
    def set_amp_enable(self, value):
        if value == True:
            val = 1
        else:
            val = 0
        result =  libhackrf.hackrf_set_amp_enable(self.device, val)
        if result == HackRfError.HACKRF_SUCCESS:
            logger.debug('Successfully set amp')
            return True
        else:
            logger.error('Failed to set amp')

    @opened
    def set_baseband_filter_bandwidth(self, bandwidth_hz):
        result = libhackrf.hackrf_set_baseband_filter_bandwidth(self.device, bandwidth_hz)
        if result != HackRfError.HACKRF_SUCCESS:
            logger.error(
                'Failed to set Baseband Filter Bandwidth with value [%d]', bandwidth_hz)
        else:
            logger.debug(
                'Successfully set Baseband Filter Bandwidth with value [%d]', bandwidth_hz)
            return True

    @opened
    def max2837_read(self, register_number, value):
        pass
        return libhackrf.hackrf_max2837_read(self.device, register_number, value)

    @opened
    def max2837_weite(self, register_number, value):
        pass
        return libhackrf.hackrf_max2837_weite(self.device, register_number, value)

    @opened
    def si5351c_read(self, register_number, value):
        pass
        return libhackrf.hackrf_si5351c_read(self.device, register_number, value)

    @opened
    def si5351c_write(self, register_number, value):
        pass
        return libhackrf.hackrf_si5351c_write(self.device, register_number, value)

    @opened
    def rffc5071_read(self, register_number, value):
        pass
        return libhackrf.hackrf_rffc5071_read(self.device, register_number, value)

    @opened
    def rffc5071_write(self, register_number, value):
        pass
        return libhackrf.hackrf_rffc5071_write(self.device, register_number, value)

    @opened
    def spiflash_erase(self):
        pass
        return libhackrf.hackrf_spiflash_erase(self.device)

    @opened
    def spiflash_write(self, address, length, data):
        pass
        return libhackrf.hackrf_spiflash_write(self.device, address, length, data)

    @opened
    def spiflash_read(self, address, length, data):
        pass
        return libhackrf.hackrf_spiflash_read(self.device, address, length, data)

    @opened
    def cpld_write(self, data, total_length):
        pass
        return libhackrf.hackrf_cpld_write(self.device, data, total_length)

    @opened
    def set_sample_rate_manual(self, freq_hz, divider):
        pass
        return libhackrf.hackrf_set_sample_rate_manual(self.device, freq_hz, divider)

    @opened
    def compute_baseband_filter_bw_round_down_lt(self, bandwidth_hz):
        pass
        return libhackrf.hackrf_compute_baseband_filter_bw_round_down_lt(bandwidth_hz)

    @opened
    def compute_baseband_filter_bw(self, bandwidth_hz):
        pass
        return libhackrf.hackrf_compute_baseband_filter_bw(bandwidth_hz)

    # def hackrf_set_freq_explicit(self, if_freq_hz, lo_freq_hz, path):
    #     pass
    # return libhackrf.hackrf_set_freq_explicit(if_freq_hz, lo_freq_hz, path)

    # def hackrf_board_partid_serialno_read(self, read_partid_serialno):
    #     pass
    # return libhackrf.hackrf_board_partid_serialno_read(read_partid_serialno)

    # def hackrf_error_name(self, errcode):
    #     pass
    #     return libhackrf.hackrf_error_name(errcode)

    # def hackrf_board_id_name(self, board_id):
    #     pass
    #     return libhackrf.hackrf_board_id_name(board_id)

    # def hackrf_filter_path_name(self, path):
    #     pass
    #     return libhackrf.hackrf_filter_path_name(path)

    @opened
    def start_rx_iq_to_queue(self, queue, size=1024):
        def callback(size, queue, hackrf_transfer):
            array_type = (c_byte * size)
            values = cast(hackrf_transfer.contents.buffer,
                          POINTER(array_type)).contents
            iq = self.packed_bytes_to_iq(values)
            queue.put(iq)
            return 0
        callback = partial(callback, size, queue)
        return self.start_rx_mode(callback)

    def packed_bytes_to_iq(self, bytes):
        dat = np.frombuffer(bytes, dtype='int8')
        iq = dat.astype(np.float32).view(np.complex64)
        return iq/128.0
