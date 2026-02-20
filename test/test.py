# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import os
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

BUILD = os.environ.get("BUILD", "counter")


@cocotb.test(skip=BUILD != "counter")
async def test_counter(dut):
    """Test tt_um_counter: 8-bit up-counter on uo_out, reset clears to 0."""
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Reset
    dut._log.info("Reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # After one cycle, counter has incremented 0 -> 1; then count 1, 2, ..., 15
    for expected in range(1, 16):
        assert dut.uo_out.value.integer == expected, (
            f"Expected {expected}, got {dut.uo_out.value.integer}"
        )
        await ClockCycles(dut.clk, 1)

    dut._log.info("Count-up test passed")

    # Reset again and verify counter clears, then counts from 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 1, f"Expected 1 after second reset, got {dut.uo_out.value.integer}"

    # Verify rollover: count from 1 to 255, next cycle should be 0
    for _ in range(253):
        await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 254
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 255
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 0, "Expected rollover 255 -> 0"

    dut._log.info("All counter tests passed")


@cocotb.test(skip=BUILD != "picosoc")
async def test_picosoc(dut):
    """Test tt_um_picosoc: reset and run; design must not hang (CPU may drive UART)."""
    dut._log.info("Start PicoSoC test")

    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    dut._log.info("Reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 100)

    # Design ran without hanging (CPU may drive UART TX low when executing)
    dut._log.info("PicoSoC test passed")
