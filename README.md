# SDG1032X Python library

This (unofficial) library allows one to control __some__ functions of the
SDG1032X arbitrary waveform generator using Python in a simple way via
Ethernet.

Exposed functionality:

| Functionality        | Function                                                           | Implemented | Tested | Comments                                      |
| -------------------- | ------------------------------------------------------------------ | ----------- | ------ | --------------------------------------------- |
| Identify             | ```identify()```                                                   | y           | y      | Queries the output of IDN, raw binary output  |
| Factory defaults     | ```factoryDefaults()```                                            | y           |        | Resets all device state to factory defaults   |
| Enable output        | ```outputEnable(channel=1, polarity=POLARITY_NORMAL, load="HZ")``` | y           | y      | Enabled the output of the function generator  |
| Disable output       | ```outputDisable(channel=1)```                                     | y           | y      | Disables the output of the function generator |
| Set duty cycle       | ```setDutyCycle(dutycycle, channel=1)```                           | y           | y      | Sets duty cycle                               |
| Enabling burst mode  | ```setBurstModeEnable(channel=1)```                                | y           | y      |                                               |
| Disabling burst mode | ```setBurstModeDisable(channel=1)```                               | y           | y      |                                               |
| Setting burst period | ```setBurstPeriod(period, channel=1)```                            | y           | y      | Burst period                                  |
| Setting burst delay  | ```setBurstDelay(delay, channel=1)```                              | y           | y      |                                               |
| Setting burst tigger | ```setBurstTriggerSource(triggerSource, channel=1)```              | y           | y      | Sets internal, external or manual trigger     |
| Setting burst mode   | ```setBurstMode(burstMode, channel=1)```                           | y           | y      |                                               |
| Triggering burst     | ```triggerBurst(channel=1)```                                      | y           |        |                                               |
| Set waveform         | ```setWaveType(waveform, channel=1)```                             | y           | y      | Sets the waveform of the signal               |
| Set frequency        | ```setWaveFrequency(frequency, channel=1)```                       | y           | y      | Sets the waves frequency                      |
| Set period           | ```setWavePeriod(period, channel=1)```                             | y           | y      | Sets the waves period                         |
| Set wave amplitude   | ```setWaveAmplitude(vpp, channel=1)```                             | y           |        | Sets the amplitude of the wave in Vpp         |
| Set wave offset      | ```setWaveOffset(offsetV, channel=1)```                            | y           |        | Sets the offset of the wave in V              |

## Usage example

```
with SDG1032X("10.0.0.14") as sdg:
    print("Identify returns: {}".format(sdg.identify()))

    sdg.setWaveType(sdg.WAVEFORM_SINE)

    for f in range(100, 1100, 100):
        sdg.setWavePeriod(f)
```

## Installation

There are two ways of simply installing the library. One can install
if via ```pip``` from PyPi:

```
pip install pysdg1032x-tspspi
```

Or one can install it from the downloaded ZIP file from the [Releases section](https://github.com/tspspi/pysdg1032x/releases)
by using pip (substituting ```X.Y.Z``` by the desired version number):

```
pip install pysdg1032x-tspspi-X.Y.Z.tar.gz
```

## The CLI utility

There is a simple CLI utility that allows one to control the function generator
from the commandline or via scripts. This tool is called ```sdg1032x```:

```
SDG1032X signal generator remote control utility

Note: This tool is an inofficial tool and in no way associated
with Siglent

Usage:
	sdg1032x [settings] <commands>

Settings:
	--host ADDRESS		Sets the remote hostname or IP

Commands:
	id			Asks the SDG for it's identity
	defaults		Resets the SDG to it's factory defaults

Simple channel commands:
	on N			Enabled the channel N
	off N			Disabled the channel N

Waveform commands:
	wavetype N WTYPE	Sets the selected wave type. Valid options are:
				sine	Sinusoidal waveform
				square	Square wave
				ramp	Ramping
				pulse	Pulsing
				noise	Noise generator
				arbitrary	Arbitrary waveform from WAV
				dc	Discrete current
				prbs	Pseudo random binary sequence
	frq N FREQ		Set frequency of channel N to FREQ Hz
	period N PERIOD		Set period of channel N to PERIOD seconds
	amp N AMP		Set amplitude of wave for channel N to AMP Vpp
	offset N OFF		Set offset of channel N to OFF V

Burst mode commands (per channel):
	duty N CYCLE		Sets the burst duty cycle for channel N to CYCLE percent
	burston N		Enables burst mode for channel N
	burstoff N		Disables burst mode for channel N
	burstperiod N PERIOD	Sets the burst period for channel N to PERIOD seconds
	burstdelay N DELAY	Sets the burst delay for channel N to DELAY seconds
	bursttrigsource N SRC	Sets the given trigger source. Valid options are:
				int	internal trigger source
				ext	external trigger source
				man	manual trigger source
	burstmode N MODE	Sets the burst mode. Valid modes are:
				gate	Gated burst mode
				ncyc	Number of cycles burst mode
	burst N			Trigger burst on channel N
```
