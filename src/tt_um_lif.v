/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_lif (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.

  wire [7:0] state_n1;
  wire [7:0] state_n2;
  wire spike_n1;
  wire spike_n2;

  //assign uio_oe  = 0;

  wire [7:0] n2_in = spike_n1 ? 8'd128 : 8'd0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in, state_n2, 1'b0};

  //instantiate the lif neuron
  lif lif1 (.current(ui_in), .clk(clk), .reset_n(rst_n), .state(state_n1), .spike(spike_n1));
  lif lif2 (.current(n2_in), .clk(clk), .reset_n(rst_n), .state(state_n2), .spike(spike_n2));
  
  assign uo_out = state_n2;
  assign uio_out[7] = spike_n2;
  assign uio_out[6] = spike_n1;
  assign uio_out[5:0] = 0;
  assign uio_oe = 8'b11000000;
  

  // lif lif2 (.current(uio_out[7]), .clk(clk), .reset_n(rst_n), .state(uo_out), .spike(uio_out[7]));
 
endmodule
