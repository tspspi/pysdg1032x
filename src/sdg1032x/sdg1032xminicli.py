#!/usr/bin/env python3
import time, sys
import textwrap

from sdg1032x.sdg1032x import SDG1032X

def printUsage():
    print(textwrap.dedent("""
        SDG1032X signal generator remote control utility

        Note: This tool is an inofficial tool and in no way associated
        with Siglent

        Usage:
        \t{} [settings] <commands>

        Settings:
        \t--host ADDRESS\t\tSets the remote hostname or IP

        Commands:
        \tid\t\t\tAsks the SDG for it's identity
        \tdefaults\t\tResets the SDG to it's factory defaults

        Simple channel commands:
        \ton N\t\t\tEnabled the channel N
        \toff N\t\t\tDisabled the channel N

        Waveform commands:
        \twavetype N WTYPE\tSets the selected wave type. Valid options are:
        \t\t\t\tsine\tSinusoidal waveform
        \t\t\t\tsquare\tSquare wave
        \t\t\t\tramp\tRamping
        \t\t\t\tpulse\tPulsing
        \t\t\t\tnoise\tNoise generator
        \t\t\t\tarbitrary\tArbitrary waveform from WAV
        \t\t\t\tdc\tDiscrete current
        \t\t\t\tprbs\tPseudo random binary sequence
        \tfrq N FREQ\t\tSet frequency of channel N to FREQ Hz
        \tperiod N PERIOD\t\tSet period of channel N to PERIOD seconds
        \tamp N AMP\t\tSet amplitude of wave for channel N to AMP Vpp
        \toffset N OFF\t\tSet offset of channel N to OFF V

        Burst mode commands (per channel):
        \tduty N CYCLE\t\tSets the burst duty cycle for channel N to CYCLE percent
        \tburston N\t\tEnables burst mode for channel N
        \tburstoff N\t\tDisables burst mode for channel N
        \tburstperiod N PERIOD\tSets the burst period for channel N to PERIOD seconds
        \tburstdelay N DELAY\tSets the burst delay for channel N to DELAY seconds
        \tbursttrigsource N SRC\tSets the given trigger source. Valid options are:
        \t\t\t\tint\tinternal trigger source
        \t\t\t\text\texternal trigger source
        \t\t\t\tman\tmanual trigger source
        \tburstmode N MODE\tSets the burst mode. Valid modes are:
        \t\t\t\tgate\tGated burst mode
        \t\t\t\tncyc\tNumber of cycles burst mode
        \tburst N\t\t\tTrigger burst on channel N
        """).format(sys.argv[0]))

def sdg1032xValidChannel(ch):
    try:
        chInt = int(ch)
        if (chInt < 1) or (chInt > 2):
            return False
    except ValueError:
        return False
    return True

def sdg1032xminicli():
    host = None
    if len(sys.argv) < 2:
        printUsage()
        return

    # Gather settings and verify all parameters are present & valid

    skipArg = 0
    for i in range(1, len(sys.argv)):
        if skipArg > 0:
            skipArg = skipArg - 1
            continue
        if sys.argv[i].strip() == "--host":
            if i == (len(sys.argv)-1):
                print("Missing hostname after --host parameter")
                sys.exit(2)
                return
            host = sys.argv[i+1]
            skipArg = 1
        elif sys.argv[i].strip() == "id":
            pass
        elif sys.argv[i].strip() == "defaults":
            pass
        elif sys.argv[i].strip() == "on":
            skipArg = 1
            if i == (len(sys.argv)-1):
                print("Missing channel number after on command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
        elif sys.argv[i].strip() == "off":
            skipArg = 1
            if i == (len(sys.argv)-1):
                print("Missing channel number after on command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
        elif sys.argv[i].strip() == "duty":
            skipArg = 2
            if (i == (len(sys.argv)-1)) or (i == (len(sys.argv)-2)):
                print("Missing burst duty cycle or channel number after duty command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
            try:
                cycle = float(sys.argv[i+2].strip())
                if (cycle < 0) or (cycle > 100):
                    raise ValueError()
            except ValueError:
                print("Invalid burst duty cycle {} after duty command (should be 0-100%)".format(sys.argv[i+1]))
                sys.exit(2)
                return
        elif sys.argv[i].strip() == "burston":
            skipArg = 1
            if i == (len(sys.argv)-1):
                print("Missing channel number after burston command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
        elif sys.argv[i].strip() == "burstoff":
            skipArg = 1
            if i == (len(sys.argv)-1):
                print("Missing channel number after burstoff command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
        elif sys.argv[i].strip() == "burstperiod":
            skipArg = 2
            if (i == (len(sys.argv)-1)) or (i == (len(sys.argv)-2)):
                print("Missing burst period or channel number after burst period command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
            try:
                cycle = float(sys.argv[i+2].strip())
            except ValueError:
                print("Invalid burst period {}".format(sys.argv[i+1]))
                sys.exit(2)
                return
        elif sys.argv[i].strip() == "burstdelay":
            skipArg = 2
            if (i == (len(sys.argv)-1)) or (i == (len(sys.argv)-2)):
                print("Missing burst duty cycle or channel number after burst delay command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
            try:
                cycle = float(sys.argv[i+2].strip())
            except ValueError:
                print("Invalid burst delay {}".format(sys.argv[i+1]))
                sys.exit(2)
                return
        elif sys.argv[i].strip() == "bursttrigsource":
            skipArg = 2
            if (i == (len(sys.argv)-1)) or (i == (len(sys.argv)-2)):
                print("Missing burst duty cycle or channel number after burst delay command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
            trSource = None
            if sys.argv[i+2].strip() == "int":
                trSource = SDG1032X.TRIGGERSOURCE_INTERNAL
            if sys.argv[i+2].strip() == "ext":
                trSource = SDG1032X.TRIGGERSOURCE_EXTERNAL
            if sys.argv[i+2].strip() == "man":
                trSource = SDG1032X.TRIGGERSOURCE_MANUAL
            if trSource == None:
                print("Invalid burst trigger source {} on channel {} (should be internal, external or manual)".format(sys.argv[i+2].strip(), ch))
        elif sys.argv[i].strip() == "burstmode":
            skipArg = 2
            if (i == (len(sys.argv)-1)) or (i == (len(sys.argv)-2)):
                print("Missing burst duty cycle or channel number after burst delay command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
            ch = int(sys.argv[i+1].strip())
            trMode = None
            if sys.argv[i+2].strip() == "gate":
                trMode = SDG1032X.BURSTMODE_GATE
            if sys.argv[i+2].strip() == "ncyc":
                trMode = SDG1032X.BURSTMODE_NCYC
            if trMode == None:
                print("Invalid burst mode {} on channel {}".format(sys.argv[i+2], ch))
        elif sys.argv[i].strip() == "burst":
            skipArg = 1
            if i == (len(sys.argv)-1):
                print("Missing channel number after burst command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
        elif sys.argv[i].strip() == "wavetype":
            skipArg = 2
            if (i == (len(sys.argv)-1)) or (i == (len(sys.argv)-2)):
                print("Missing burst duty cycle or channel number after burst delay command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
            wType = None
            if (sys.argv[i+2].strip() == "sine") or (sys.argv[i+2].strip() == "sin"):
                wType = SDG1032X.WAVEFORM_SINE
            elif sys.argv[i+2].strip() == "square":
                wType = SDG1032X.WAVEFORM_SQUARE
            elif sys.argv[i+2].strip() == "ramp":
                wType = SDG1032X.WAVEFORM_RAMP
            elif sys.argv[i+2].strip() == "pulse":
                wType = SDG1032X.WAVEFORM_PUSLE
            elif sys.argv[i+2].strip() == "noise":
                wType = SDG1032X.WAVEFORM_NOISE
            elif sys.argv[i+2].strip() == "arbitrary":
                wType = SDG1032X.WAVEFORM_ARBITRARY
            elif sys.argv[i+2].strip() == "dc":
                wType = SDG1032X.WAVEFORM_DC
            elif sys.argv[i+2].strip() == "prbs":
                wType = SDG1032X.WAVEFORM_PSEUDORANDOMBINARY
            if wType == None:
                print("Unknown waveform {}".format(sys.argv[i+2].strip()))
        elif sys.argv[i].strip == "frq":
            skipArg = 2
            if (i == (len(sys.argv)-1)) or (i == (len(sys.argv)-2)):
                print("Missing burst duty cycle or channel number after burst delay command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
            try:
                frq = float(sys.argv[i+2])
                if frq <= 0:
                    raise ValueError()
            except ValueError:
                print("Invalid channel {} frequency {}".format(ch, sys.argv[i+2]))
        elif sys.argv[i].strip() == "period":
            skipArg = 2
            if (i == (len(sys.argv)-1)) or (i == (len(sys.argv)-2)):
                print("Missing burst duty cycle or channel number after burst delay command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
            try:
                frq = float(sys.argv[i+2])
                if frq <= 0:
                    raise ValueError()
            except ValueError:
                print("Invalid channel {} period {}".format(ch, sys.argv[i+2]))
        elif sys.argv[i].strip() == "amp":
            skipArg = 2
            if (i == (len(sys.argv)-1)) or (i == (len(sys.argv)-2)):
                print("Missing amplitude or channel number after wave amplitude command")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
            try:
                amp = float(sys.argv[i+2])
                if amp <= 0:
                    raise ValueError()
            except ValueError:
                print("Invalid channel {} amplitude {} Vpp".format(ch, sys.argv[i+2]))
        elif sys.argv[i].strip() == "offset":
            skipArg = 2
            if (i == (len(sys.argv)-1)) or (i == (len(sys.argv)-2)):
                print("Missing offset or channel number after wave offset")
                sys.exit(2)
                return
            if not sdg1032xValidChannel(sys.argv[i+1].strip()):
                print("Invalid channel {} for SDG".format(sys.argv[i+1].strip()))
                sys.exit(2)
                return
            try:
                offset = float(sys.argv[i+2])
            except ValueError:
                print("Invalid channel {} offset {} V".format(ch, sys.argv[i+2]))
        elif sys.argv[i].strip() == "sleep":
            skipArg = 1
            if i == (len(sys.argv)-1):
                print("Missing duration after sleep command")
                sys.exit(2)
                return
            try:
                durationsecs = int(sys.argv[i+1])
                if durationsecs <= 0:
                    raise ValueError()
            except ValueError:
                print("Invalid number of seconds {} on sleep".format(durationsecs))


    # Run commands ...
    if host == None:
        print("No host specified")
        sys.exit(1)

    try:
        with SDG1032X(host) as sdg:
            skipArg = 0
            for i in range(1, len(sys.argv)):
                if skipArg > 0:
                    skipArg = skipArg - 1
                    continue
                if sys.argv[i].strip() == "--host":
                    skipArg = 1
                    continue
                if sys.argv[i].strip() == "id":
                    print("Identifying device:")
                    res = sdg.identify()
                    print(res)
                if sys.argv[i].strip() == "defaults":
                    print("Setting factory defaults")
                    sdg.factoryDefaults()
                if sys.argv[i].strip() == "on":
                    skipArg = 1
                    ch = int(sys.argv[i+1].strip())
                    print("Enabling channel {}".format(ch))
                    sdg.outputEnable(ch)
                if sys.argv[i].strip() == "off":
                    skipArg = 1
                    ch = int(sys.argv[i+1].strip())
                    print("Disabling channel {}".format(ch))
                    sdg.outputDisable(ch)
                if sys.argv[i].strip() == "duty":
                    skipArg = 2
                    ch = int(sys.argv[i+1].strip())
                    cycle = float(sys.argv[i+2].strip())
                    print("Setting burst duty cycle for channel {} to {}%".format(ch, cycle))
                    sdg.setDutyCycle(cycle, ch)
                if sys.argv[i].strip() == "burston":
                    skipArg = 1
                    ch = int(sys.argv[i+1].strip())
                    print("Enabling burst mode on channel {}".format(ch))
                    sdg.setBurstModeEnable(ch)
                if sys.argv[i].strip() == "burstoff":
                    skipArg = 1
                    ch = int(sys.argv[i+1].strip())
                    print("Disabling burst mode on channel {}".format(ch))
                    sdg.setBurstModeDisable(ch)
                if sys.argv[i].strip() == "burstperiod":
                    skipArg = 2
                    ch = int(sys.argv[i+1].strip())
                    period = float(sys.argv[i+2].strip())
                    print("Setting burst period for channel {} to {}s".format(ch, period))
                    sdg.setBurstPeriod(period, ch)
                if sys.argv[i].strip() == "burstdelay":
                    skipArg = 2
                    ch = int(sys.argv[i+1].strip())
                    delay = float(sys.argv[i+2].strip())
                    print("Setting burst delay for channel {} to {}s".format(ch, delay))
                    sdg.setBurstDelay(delay, ch)
                if sys.argv[i].strip() == "bursttrigsource":
                    skipArg = 2
                    ch = int(sys.argv[i+1].strip())
                    if sys.argv[i+2].strip() == "int":
                        trSource = sdg.TRIGGERSOURCE_INTERNAL
                        trSourceStr = "internal"
                    if sys.argv[i+2].strip() == "ext":
                        trSource = sdg.TRIGGERSOURCE_EXTERNAL
                        trSourceStr = "external"
                    if sys.argv[i+2].strip() == "man":
                        trSource = sdg.TRIGGERSOURCE_MANUAL
                        trSourceStr = "manual"
                    print("Setting channel {} burst trigger source to {}".format(ch, trSourceStr))
                    sdg.setBurstTriggerSource(trSource, ch)
                if sys.argv[i].strip() == "burstmode":
                    skipArg = 2
                    ch = int(sys.argv[i+1].strip())
                    if sys.argv[i+2].strip() == "gate":
                        trMode = sdg.BURSTMODE_GATE
                        trModeStr = "gated"
                    if sys.argv[i+2].strip() == "ncyc":
                        trMode = sdg.BURSTMODE_NCYC
                        trModeStr = "number of cycles"
                    print("Setting channel {} burst mode to {}".format(ch, trModeStr))
                    sdg.setBurstMode(trMode, ch)
                if sys.argv[i].strip() == "burst":
                    skipArg = 1
                    ch = int(sys.argv[i+1].strip())
                    print("Triggering burst on channel {}".format(ch))
                    sdg.triggerBurst(ch)
                if sys.argv[i].strip() == "wavetype":
                    skipArg = 2
                    ch = int(sys.argv[i+1].strip())
                    wType = None
                    if (sys.argv[i+2].strip() == "sine") or (sys.argv[i+2].strip() == "sin"):
                        wType = sdg.WAVEFORM_SINE
                        wTypeStr = "sine"
                    elif sys.argv[i+2].strip() == "square":
                        wType = sdg.WAVEFORM_SQUARE
                        wTypeStr = "square wave"
                    elif sys.argv[i+2].strip() == "ramp":
                        wType = sdg.WAVEFORM_RAMP
                        wTypeStr = "ramp"
                    elif sys.argv[i+2].strip() == "pulse":
                        wType = sdg.WAVEFORM_PUSLE
                        wTypeStr = "pulse"
                    elif sys.argv[i+2].strip() == "noise":
                        wType = sdg.WAVEFORM_NOISE
                        wTypeStr = "noise"
                    elif sys.argv[i+2].strip() == "arbitrary":
                        wType = sdg.WAVEFORM_ARBITRARY
                        wTypeStr = "arbitrary"
                    elif sys.argv[i+2].strip() == "dc":
                        wType = sdg.WAVEFORM_DC
                        wTypeStr = "DC"
                    elif sys.argv[i+2].strip() == "prbs":
                        wType = sdg.WAVEFORM_PSEUDORANDOMBINARY
                        wTypeStr = "pseudo random binary sequence"
                    print("Setting channel {} waveform to {}".format(ch, wTypeStr))
                    sdg.setWaveType(wType, ch)
                if sys.argv[i].strip() == "frq":
                    skipArg = 2
                    ch = int(sys.argv[i+1].strip())
                    frq = float(sys.argv[i+2].strip())
                    print("Setting channel {} frequency to {}Hz".format(ch, frq))
                    sdg.setWaveFrequency(frq, ch)
                if sys.argv[i].strip() == "period":
                    skipArg = 2
                    ch = int(sys.argv[i+1].strip())
                    p = float(sys.argv[i+2].strip())
                    print("Setting channel {} period to {}s".format(ch, p))
                    sdg.setWavePeriod(p, ch)
                if sys.argv[i].strip() == "amp":
                    skipArg = 2
                    ch = int(sys.argv[i+1].strip())
                    amp = float(sys.argv[i+2].strip())
                    print("Setting channel {} amplitude to {} Vpp".format(ch, amp))
                    sdg.setWaveAmplitude(amp, ch)
                if sys.argv[i].strip() == "offset":
                    skipArg = 2
                    ch = int(sys.argv[i+1].strip())
                    offset = float(sys.argv[i+2].strip())
                    print("Setting channel {} offset to {} Vpp".format(ch, offset))
                    sdg.setWaveOffset(offset, ch)
                if sys.argv[i].strip() == "sleep":
                    skipArg = 1
                    durationsecs = int(sys.argv[i+1].strip())
                    print("Sleeping for {} seconds".format(durationsecs))
                    time.sleep(durationsecs)



    except Exception as e:
        print(e)
        pass

if __name__ == "__main__":
    sdg1032xminicli()
