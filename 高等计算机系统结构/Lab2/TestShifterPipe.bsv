import RightShifterTypes::*;
import RightShifter::*;
import FIFO::*;

(* synthesize *)
module mkTests (Empty);
   RightShifterPipelined rsp <- mkRightShifterPipelined;
   Reg#(Bit#(32)) tbCounter <- mkReg(0);
   FIFO#(Bit#(32)) answerFifo <- mkSizedFIFO(6);
   
   // there are many ways to write tests.  Here is a very simple
   // version, just to get you started.

   rule run;
	rsp.push(LogicalRightShift, tbCounter, 1);
	answerFifo.enq(tbCounter >> 1);
	tbCounter <=tbCounter + 1;
   endrule

   rule test;

      let b <- rsp.pull();
      let answer = answerFifo.first();
      answerFifo.deq();

      if (b != answer) begin
	 $display("result is ", b, " but expected ", answer);
      end
      else begin
	 $display("correct!");
      end

      if (tbCounter > 13) $finish(0);

   endrule
endmodule
