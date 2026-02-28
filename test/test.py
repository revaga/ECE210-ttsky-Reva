# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_lif(dut):
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
    n1_spike = False

    for i in range(10):
        await RisingEdge(dut.clk)
        if int(dut.uio_out.value) & 0x40: # 0x40 is the 64 bit
            n1_spike = True
            break

    assert n1_spike, "n1 did not spike"

    await RisingEdge(dut.clk)
    n2_state = int(dut.uo_out.value)

    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 5)
    assert int(dut.uo_out.value) == 128, "n2 state changes"

    dut.ui_in.value = 210
    spike_detected = False
    for _ in range(20):
        await RisingEdge(dut.clk)
        if int(dut.uio_out.value) & 0x80: # 0x40 is the 64 bit
            spike_detected = True
            break

    assert spike_detected, "n2 did not spike"

    await RisingEdge(dut.clk)
    assert int(dut.uo_out.value) == 0, "n2 didn't reset after spiking"

    dut._log.info("yipee!!")