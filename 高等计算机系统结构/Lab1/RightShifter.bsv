import RightShifterTypes::*;
import Gates::*;

function Bit#(1) multiplexer1(Bit#(1) sel, Bit#(1) a, Bit#(1) b);
	// Part 1: Re-implement this function using the gates found in the Gates.bsv file
	// return (sel == 0)?a:b;
  // 使用与或非门实现这条语句，对return a&~sel | b&sel 即可
  let a_out = andGate(a,notGate(sel));
  let b_out = andGate(b,sel);
  let res = orGate(a_out , b_out);
  return res;
  
endfunction

function Bit#(32) multiplexer32(Bit#(1) sel, Bit#(32) a, Bit#(32) b);
	// Part 2: Re-implement this function using static elaboration (for-loop and multiplexer1)
	// return (sel == 0)?a:b; 
  Bit#(32) aggregate = 0;
  for(Integer i = 0; i < 32; i = i + 1)
    begin
      aggregate[i] = multiplexer1(sel, a[i], b[i]);
    end
  return aggregate;
endfunction

function Bit#(n) multiplexerN(Bit#(1) sel, Bit#(n) a, Bit#(n) b);
	// Part 3: Re-implement this function as a polymorphic function using static elaboration
	// return (sel == 0)?a:b;
  Bit#(n) aggregate = 0;
  for(Integer i = 0; i < valueof(n); i = i + 1)
    begin
      aggregate[i] = multiplexer1(sel, a[i], b[i]);
    end
  return aggregate;  
endfunction

function Bit#(n) copy_frontnum(Bit#(1) sign , Integer num);
  Bit#(n) result = 0;
  for(Integer i = 0;i < num;i = i+1)
    begin
      result[i] = sign;
    end
    return result;
endfunction

module mkRightShifter (RightShifter);
    method Bit#(32) shift(ShiftMode mode, Bit#(32) operand, Bit#(5) shamt);
	// Parts 4 and 5: Implement this function with the multiplexers you implemented
  // pack函数用于将各种Bit数据类型（例如Bool，Int或UInt）转换（或打包）为（Bit＃（n））类型。
        Bit#(32) result = 0;
        Bit#(1) flag = 0;
        Bit#(1) sign_bit = operand[31];
        // flag用来判断是逻辑还是算数右移，逻辑右移前面补0，算数右移前面补符号位。
        if(mode == LogicalRightShift)
          begin
            flag = 1;
          end
        // 确定要右移前面要填充的0 OR 1
        sign_bit = multiplexerN(flag , operand[31] , 0);
        // 按照位置右移
        result = multiplexerN( shamt[0] , operand, {sign_bit,operand[31:1]});
    	result = multiplexerN( shamt[1] , result, {copy_frontnum(sign_bit,2),result[31:2]});
    	result = multiplexerN( shamt[2] , result, {copy_frontnum(sign_bit,4),result[31:4]});
    	result = multiplexerN( shamt[3] , result, {copy_frontnum(sign_bit,8),result[31:8]});
    	result = multiplexerN( shamt[4] , result, {copy_frontnum(sign_bit,16),result[31:16]});
        
        return result;   
    endmethod
endmodule
