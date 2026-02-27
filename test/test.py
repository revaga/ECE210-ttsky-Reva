# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_lif_behavior(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="ns") 
    cocotb.start_soon(clock.start())


    dut.rst_n.value = 0; # low to reset
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.ena.value = 1
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    # iin > 100 to overcome 1/2 leak and hit 200 threshold for spiking
    dut.ui_in.value = 110 
    
    dut._log.info("Testing integration with input 110...")
    for i in range(5):
        await RisingEdge(dut.clk)
        state_val = int(dut.uo_out.value)
        dut._log.info(f"Cycle {i}: State = {state_val}")
        
    # test spiking
    dut.ui_in.value = 255 # Max input to spike quicker
    

    max_cycles = 50
    spike_detected = False
    
    for _ in range(max_cycles):
        await RisingEdge(dut.clk)
        if int(dut.uio_out.value) & 0x80: # 0x80 is the 128 bit
            spike_detected = True
            dut._log.info(f"spike at {int(dut.uo_out.value)}")
            break
            
    assert spike_detected, "no spike w/ 50 cycles"

    # test leaking (w/ zero input)
    dut.ui_in.value = 0
    await RisingEdge(dut.clk)
    pre_leak = int(dut.uo_out.value)
    await RisingEdge(dut.clk)
    post_leak = int(dut.uo_out.value)
    
    assert post_leak < pre_leak, "no decay with 0 input"

    dut._log.info("yipee!!")