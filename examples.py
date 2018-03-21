#!/usr/bin/env python

from time import sleep
from pylibhackrf import HackRf
from multiprocessing import Manager

hackrf = HackRf()

if hackrf.setup():
    hackrf.set_freq(100 * 1000 * 1000)
    hackrf.set_sample_rate(8 * 1000 * 1000)
    hackrf.set_amp_enable(False)
    hackrf.set_lna_gain(16)
    hackrf.set_vga_gain(20)
    queue = Manager().Queue()
    hackrf.start_rx_iq_to_queue(queue, 128)
    sleep(.5)
    hackrf.stop_rx_mode()
    print(queue.get())
