# sm4file

sm4file is Python library for reading RHK .sm4 files.

## Installing

Installation via [pip](https://pip.pypa.io/en/stable/):

```bash
pip install sm4file
```

## Example Usage

```python
from sm4file import Sm4


sm4 = Sm4("path/to/sm4-file")
```

This return a list of all acquired measurement channels. Metadata can be
accessed as properties on a channel. For example to print the bias voltage for
all channels:

```python
for channel in sm4:
    print(channel.bias)
```

The measurement's numerical data is stored in the `data` property on each
channel. For images this is a two dimensional numpy array. For lines / spectra
it is a (n, m) where n is the number of acquired data points and m is the
number of spectra + 1.
The array's first column contains the x-values and all subsequent ones the
corresponding y-values.


#### Plot images from all channels

```python
import matplotlib.pyplot as plt


for channel in sm4:
    plt.imshow(channel.data)
    plt.title(f"{channel.label} - {channel.scan_direction}")
    plt.show()
```
  

#### Plot all spectra, e.g. IV

```python
for channel in sm4:
    for i in range(1, len(channel.data[0])):
        plt.plot(channel.data[:, 0], channel.data[:, i], label=f"{i}")
        plt.title(channel.label)
        plt.legend()

    plt.show()
```
