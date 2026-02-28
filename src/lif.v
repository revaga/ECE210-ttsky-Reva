`default_nettype none

module lif (
    input wire [7:0] current,
    input wire  clk,
    input wire reset_n,
    output reg [7:0] state,
    output wire spike
);

    wire [7:0] next_state;
    reg [7:0] threshold;
    //reg [7:0] beta;

    //spiking logic
    assign spike = (state >= threshold); 

    wire [8:0] sum = current + state;
    assign next_state = (sum > 9'd255) ? 8'd255 : sum[7:0];

    always @(posedge clk) begin
        if (!reset_n) begin
            state <= 0;
            threshold <= 200; //full range is 0-256
            //beta <= 10; // numbers are usually decimal, but make it be frac, binary etc
        end else if (spike) begin
            state <= 0;
        end else begin
            state <= next_state;
        end
    end

    //next state logic
    //assign next_state = current  // +  (state >> 1); //without beta is integrate fire neuron (no leaking)
    //instead of beta * state, we just do a right shift by 1 (divide by 2)

endmodule
