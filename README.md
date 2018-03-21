pyhackrf-ctypes
==============
pyhackrf-ctypes is a Python wrapper for libhackrf.<br>
I create this project because  I want a simple Python interface to my hackrf board and pyusb is too slow for hackrf.

# Dependencies

* NumPy
* Python 2.7.x/3.3+
* [libhackrf](https://github.com/mossmann/hackrf/tree/master/host)

        sudo apt-get install python-dev,libusb-1.0-0 



## Examples

```python
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
```

# Todo
There are a few remaining functions in libhackrf  haven't been wrapped.

# License
Do What The Fuck You Want To Public License.
