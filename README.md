# Glitching-STIH237-SOCs

The script tries to unblock communication in jtag between the secured sentinel and the user's host, which turns out to be impossible to do due to multiple verification of sentinel 0xbeefface registers. The above attack is a proof-of-concept code that shows that even if the manufacturer of the secure SOC did not apply protection against the execution of a glitch at the hardware level, it can block the possibility of correct execution of the glitch by using multiple verification of sentinel registers. STIH237 used in dvb set-top-box, iptv players remains a safe product.

Faulty glitched answers:

CPU_RESET
GLITCH STATUS: width = 325, delay = 38783000
Data received:
SDI [ERROR] :: [SERVER] serviceASEMode: Sentinel not found (0x00090009 != 0xbeefface)

GLITCH STATUS: width = 353, delay = 38692500
Data received:
SDI [ERROR] :: [SERVER] serviceASEMode: Sentinel not found (0x89fc70ff != 0xbeefface)

Correct answers 0xbeefface != 0xbeefface

Other security layers used by this SOC vendor:

1.random clocks

2.clock can run statically before sentinel initialization and during sentinel initialization and verification of sensitive data it is switched to secure mode (random clock)

3.encrypted secure boot with triple time signature verification

4.the signature verification procedure also starts a random clock during its execution.

5.the external clock input is verified and blocked from possible manipulation.

6.ram scrambling.
