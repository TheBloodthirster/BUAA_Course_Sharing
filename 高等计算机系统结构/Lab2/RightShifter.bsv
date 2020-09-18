import RightShifterTypes::*;
import Gates::*;
import FIFO::*;

// 坑一：Lab1是return (sel == 0)?a:b;这里代码变成return (sel == 1)?a:b这不是坑人？
function Bit#(1) multiplexer1(Bit#(1) sel, Bit#(1) a, Bit#(1) b);
    return orGate(andGate(a, notGate(sel)),andGate(b, sel)); 
endfunction

function Bit#(32) multiplexer32(Bit#(1) sel, Bit#(32) a, Bit#(32) b);
	Bit#(32) res_vec = 0;
	for (Integer i = 0; i < 32; i = i+1)
	    begin
		res_vec[i] = multiplexer1(sel, a[i], b[i]);
	    end
	return res_vec; 
endfunction

function Bit#(n) multiplexerN(Bit#(1) sel, Bit#(n) a, Bit#(n) b);
	Bit#(n) res_vec = 0;
	for (Integer i = 0; i < valueof(n); i = i+1)
	    begin
		res_vec[i] = multiplexer1(sel, a[i], b[i]);
	    end
	return res_vec; 
endfunction

// 上一个Lab1编写的复制函数
function Bit#(n) copy_frontnum(Bit#(1) sign , Integer num);
  Bit#(n) result = 0;
  for(Integer i = 0;i < num;i = i+1)
    begin
      result[i] = sign;
    end
    return result;
endfunction

module mkRightShifterPipelined (RightShifterPipelined);
    FIFO#(Bit#(1)) high_num <- mkFIFO();
    FIFO#(Bit#(5)) shift_num <- mkFIFO();
    FIFO#(Bit#(32)) op_num <- mkFIFO();
    FIFO#(Bit#(38)) step_for_shift_1 <- mkFIFO();
    FIFO#(Bit#(38)) step_for_shift_2 <- mkFIFO();
    FIFO#(Bit#(38)) step_for_shift_4 <- mkFIFO();
    FIFO#(Bit#(38)) step_for_shift_8 <- mkFIFO();
    FIFO#(Bit#(38)) step_for_shift_16 <- mkFIFO();
    
    // 处理右移1位的规则，让流水线能够分段处理5种位移情况。
    rule step1 (True);
      Bit#(32) operand = op_num.first();
      Bit#(5) shamt = shift_num.first();
      Bit#(1) high_bit = high_num.first();
      
      let result = multiplexerN(shamt[0] , operand , {high_bit,operand[31:1]});
      // 存储流水线step的结果
      step_for_shift_1.enq({high_bit,shamt,result});
      high_num.deq();
      op_num.deq();
      shift_num.deq();
      
    endrule
    
    // 处理右移2位的规则
    rule step2 (True);
      Bit#(32) result = step_for_shift_1.first()[31:0];
      Bit#(5) shamt = step_for_shift_1.first()[36:32];
      Bit#(1) high_bit = step_for_shift_1.first()[37];

      result = multiplexerN(shamt[1] , result , {copy_frontnum(high_bit,2),result[31:2]});
      
      step_for_shift_2.enq({high_bit,shamt,result});
      step_for_shift_1.deq();
    endrule
    
    // 处理右移4位的规则
    rule step3 (True);
      Bit#(32) result = step_for_shift_2.first()[31:0];
      Bit#(5) shamt = step_for_shift_2.first()[36:32];
      Bit#(1) high_bit = step_for_shift_2.first()[37];

      result = multiplexerN(shamt[2] , result , {copy_frontnum(high_bit,4),result[31:4]});
      
      step_for_shift_4.enq({high_bit,shamt,result});
      step_for_shift_2.deq();
    endrule
    
    // 处理右移8位的规则
    rule step4 (True);
      Bit#(32) result = step_for_shift_4.first()[31:0];
      Bit#(5) shamt = step_for_shift_4.first()[36:32];
      Bit#(1) high_bit = step_for_shift_4.first()[37];

      result = multiplexerN(shamt[3] , result , {copy_frontnum(high_bit,8),result[31:8]});
      
      step_for_shift_8.enq({high_bit,shamt,result});
      step_for_shift_4.deq();
    endrule
    
    // 处理右移16位的规则
    rule step5 (True);
      Bit#(32) result = step_for_shift_8.first()[31:0];
      Bit#(5) shamt = step_for_shift_8.first()[36:32];
      Bit#(1) high_bit = step_for_shift_8.first()[37];

      result = multiplexerN(shamt[4] , result , {copy_frontnum(high_bit,16),result[31:16]});
      
      step_for_shift_16.enq({high_bit,shamt,result});
      step_for_shift_8.deq();
    endrule
    
    
    method Action push(ShiftMode mode, Bit#(32) operand, Bit#(5) shamt);
  	/* Write your code here */
      // Action push操作输入右移的类别、右移数字、右移位数
      Bit#(1) sign_bit = operand[31];
      Bit#(1) flag = 0;
      // 按照Lab1的思路进行：逻辑右移补0，算术右移补符号位
      if(mode == LogicalRightShift)
        begin
          flag = 1;
        end
      sign_bit = multiplexerN(flag , sign_bit , 0);
      
      // 把计算出来的数字和参数入队列
      high_num.enq(sign_bit);
      op_num.enq(operand);
      shift_num.enq(shamt);
    
    endmethod
	
    method ActionValue#(Bit#(32)) pull();
  	/* Write your code here */
      // ActionValue这里返回右移的结果
      Bit#(32) result = step_for_shift_16.first()[31:0];
      step_for_shift_16.deq();
      return result;
      endmethod

endmodule