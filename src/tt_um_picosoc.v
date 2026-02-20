/*
 * Tiny Tapeout wrapper for PicoSoC (PicoRV32 + RAM + UART + SPI flash interface)
 *
 * Pin mapping:
 *   ui_in[0]   -> UART RX (ser_rx)
 *   uo_out[0]  -> UART TX (ser_tx)
 *   uo_out[7:1] -> unused (0)
 *   uio_*      -> unused; flash/GPIO can be mapped here later
 *
 * Build: include picosoc.v, picorv32.v, spimemio.v, simpleuart.v before this file.
 * Compile order: simpleuart.v, spimemio.v, picosoc.v, picorv32.v, tt_um_picosoc.v
 */

`default_nettype none

module tt_um_picosoc (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    wire        iomem_valid;
    wire        iomem_ready;
    wire [ 3:0] iomem_wstrb;
    wire [31:0] iomem_addr;
    wire [31:0] iomem_wdata;
    wire [31:0] iomem_rdata;

    wire ser_tx, ser_rx;
    wire flash_csb, flash_clk;
    wire flash_io0_oe, flash_io1_oe, flash_io2_oe, flash_io3_oe;
    wire flash_io0_do, flash_io1_do, flash_io2_do, flash_io3_do;
    wire flash_io0_di, flash_io1_di, flash_io2_di, flash_io3_di;

    // Hold in reset when design not selected (ena low)
    wire resetn = rst_n & ena;

    // No external IO device on template: acknowledge and return 0
    assign iomem_ready = 1'b1;
    assign iomem_rdata = 32'b0;

    // No external flash on chip: tie flash data inputs to 0
    assign flash_io0_di = 1'b0;
    assign flash_io1_di = 1'b0;
    assign flash_io2_di = 1'b0;
    assign flash_io3_di = 1'b0;

    picosoc soc (
        .clk         (clk),
        .resetn      (resetn),

        .iomem_valid (iomem_valid),
        .iomem_ready (iomem_ready),
        .iomem_wstrb (iomem_wstrb),
        .iomem_addr  (iomem_addr),
        .iomem_wdata (iomem_wdata),
        .iomem_rdata (iomem_rdata),

        .irq_5       (1'b0),
        .irq_6       (1'b0),
        .irq_7       (1'b0),

        .ser_tx      (ser_tx),
        .ser_rx      (ser_rx),

        .flash_csb   (flash_csb),
        .flash_clk   (flash_clk),

        .flash_io0_oe (flash_io0_oe),
        .flash_io1_oe (flash_io1_oe),
        .flash_io2_oe (flash_io2_oe),
        .flash_io3_oe (flash_io3_oe),

        .flash_io0_do (flash_io0_do),
        .flash_io1_do (flash_io1_do),
        .flash_io2_do (flash_io2_do),
        .flash_io3_do (flash_io3_do),

        .flash_io0_di (flash_io0_di),
        .flash_io1_di (flash_io1_di),
        .flash_io2_di (flash_io2_di),
        .flash_io3_di (flash_io3_di)
    );

    // Tiny Tapeout dedicated pins: UART on bit 0
    assign uo_out[0]   = ser_tx;
    assign uo_out[7:1] = 7'b0;

    assign ser_rx = ui_in[0];

    // Bidirectional IO unused for now (can expose flash or GPIO later)
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;
endmodule
