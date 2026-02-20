# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_counter(dut):
    """Test tt_um_counter: 8-bit up-counter on uo_out, reset clears to 0."""
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Reset: counter should go to 0
    dut._log.info("Reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # After reset release, first cycle output is 0 (registered on posedge)
    assert dut.uo_out.value.integer == 0, f"Expected 0 after reset, got {dut.uo_out.value.integer}"

    # Count up: 1, 2, 3, ...
    for expected in range(1, 16):
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value.integer == expected, (
            f"Expected {expected}, got {dut.uo_out.value.integer}"
        )

    dut._log.info("Count-up test passed")

    # Reset again and verify counter returns to 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 0, f"Expected 0 after second reset, got {dut.uo_out.value.integer}"

    # Verify rollover: count to 255, next cycle should be 0
    for _ in range(254):
        await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 254
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 255
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 0, "Expected rollover 255 -> 0"

    dut._log.info("All counter tests passed")
