<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

It takes input voltages and treats that as the input current injection to the LIF neuron


## How to test

Apply input to ui_in and check uo_out for accumulation of internal state. 
ex: Set ui_in to a spike-inducing value (like 110) then uio_out[6] goes high.
    neuron 2's state increases by 128 after spike (uo_out == 128). repeat then uio_out[7] fires only after second spike

## External hardware
N/A