import RightShifterTypes::*;
import RightShifter::*;

(* synthesize *)
module mkTests (Empty);
   RightShifter logicalShifter <- mkRightShifter;
   RightShifter arithmeticShifter <- mkRightShifter;
   
   // there are many ways to write tests.  Here is a very simple
   // version, just to get you started.
   
   rule test;

      let g = multiplexer1(1, 1, 0);
      if (g != 0) begin
	 $display("result is ", g, " but expected 0");
      end
      else begin
	 $display("correct!");
      end
   
      let c = logicalShifter.shift(LogicalRightShift, 12, 2);
      if (c != 3) begin
	 $display("result is ", c, " but expected 3");
      end
      else begin
	 $display("correct!");
      end

      let b = logicalShifter.shift(LogicalRightShift, 12, 1);
      if (b != 6) begin
	 $display("result is ", b, " but expected 6");
      end
      else begin
	 $display("correct!");
      end

      let a = logicalShifter.shift(LogicalRightShift, 1, 1);
      if (a != 0) begin
	 $display("result is ", a); 
      end
      else begin
	 $display("correct!");
      end
      
      let h = logicalShifter.shift(ArithmeticRightShift, 12, 2);
      if (h != 3) begin
	 $display("result is ", h, " but expected 3");
      end
      else begin
	 $display("correct!");
      end

      let i = logicalShifter.shift(LogicalRightShift, -32, 3);
      if (i != 536870908) begin
	 $display("result is ", i, " but expected 536870908");
      end
      else begin
	 $display("correct!");
      end
      
      let p = logicalShifter.shift(ArithmeticRightShift, -32, 3);
      if (p != -4) begin
	 $display("result is ", p, " but expected -4");
      end
      else begin
	 $display("correct!");
      end

      $finish(0);
   endrule
endmodule
