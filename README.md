# SDG1032X Python library

This (unofficial) library allows one to control some functions of the
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
