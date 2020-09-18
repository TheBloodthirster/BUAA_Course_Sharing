/*

Copyright (C) 2012

Arvind <arvind@csail.mit.edu>
Derek Chiou <derek@ece.utexas.edu>
Muralidaran Vijayaraghavan <vmurali@csail.mit.edu>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*/


import Types::*;
import ProcTypes::*;
import MemTypes::*;
import RFile::*;
import IMemory::*;
import DMemory::*;
import Decode::*;
import Exec::*;
import Cop::*;

// 加入写回状态，还有wb_ir存状态指令
typedef enum {Fetch,Execute,WriteBack} State deriving (Bits, Eq);

interface Proc;
   method ActionValue#(Tuple2#(RIndx, Data)) cpuToHost;
   method Action hostToCpu(Bit#(32) startpc);
endinterface

(* synthesize *)
module [Module] mkProc(Proc);
  Reg#(Addr) pc <- mkRegU;
  RFile      rf <- mkRFile;
  IMemory  iMem <- mkIMemory;
  DMemory  dMem <- mkDMemory;
  Cop       cop <- mkCop;
  
  Reg#(State) state <- mkReg(Fetch);
  Reg#(Data)     ir <- mkRegU;
  Reg#(ExecInst) wb_ir <- mkRegU;
  // 取值
  rule doFetch(cop.started && state == Fetch);
    let inst = iMem.req(pc);

    $display("pc: %h inst: (%h) expanded: ", pc, inst, showInst(inst));

    // store the instruction in a register 将指令存储在寄存器中
    ir <= inst;

    // switch to execute state 切换到执行状态
    state <= Execute;
  endrule
  // 执行状态做译码，读寄存器，执行，内存操作
  rule doExecute(cop.started && state == Execute);
    let inst = ir;
    // 解码
    let dInst = decode(inst);
    
    // 读取寄存器的值
    let rVal1 = rf.rd1(validRegValue(dInst.src1));
    let rVal2 = rf.rd2(validRegValue(dInst.src2));  
       
    // 读取协处理器以进行调试
    let copVal = cop.rd(validRegValue(dInst.src1));
    
    // 执行
    // 第五个参数是预测的PC，用来检测是否被预测错误。
    // 由于没有分支预测，因此以随机值发送字段
    let eInst = exec(dInst, rVal1, rVal2, pc, ?, copVal);
    
    // 执行不受支持的指令，退出
    if(eInst.iType == Unsupported)
    begin
      $fwrite(stderr, "Executing unsupported instruction at pc: %x. Exiting\n", pc);
      $finish;
    end
    
    // 内存操作
    if(eInst.iType == Ld)
    begin
      let data <- dMem.req(MemReq{op: Ld, addr: eInst.addr, byteEn: ?, data: ?});
      eInst.data = gatherLoad(eInst.addr, eInst.byteEn, eInst.unsignedLd, data);
    end
    else if(eInst.iType == St)
    begin
      match {.byteEn, .data} = scatterStore(eInst.addr, eInst.byteEn, eInst.data);
      let d <- dMem.req(MemReq{op: St, addr: eInst.addr, byteEn: byteEn, data: data});
    end
    
    //// 旧写回
    //if (isValid(eInst.dst) && validValue(eInst.dst).regType == Normal)
    //  rf.wr(validRegValue(eInst.dst), eInst.data);
    //// 根据是否使用分支来更新PC
    //pc <= eInst.brTaken ? eInst.addr : pc + 4;
    //// 协处理器写调试和统计信息
    //cop.wr(eInst.dst, eInst.data);
    //// switch back to fetch
    //state <= Fetch;
    
    // 新写回：判读是否进入写回阶段，否则进行正确性检查并且pc+4,状态转移取指
    if (isValid(eInst.dst) && validValue(eInst.dst).regType == Normal)
      begin
        wb_ir <= eInst;
        state <= WriteBack;
      end
    else
      begin
        pc <= eInst.brTaken ? eInst.addr : pc + 4;
        
        cop.wr(eInst.dst, eInst.data);
        
        state <= Fetch;
      end
  endrule
  
  // 实验三思路:题目要求把写回拆出来变成三阶段
  // 那么只要修改上面的写回部分代码，并且创建一个rule负责写回功能即可
  rule doWriteBack(cop.started && state == WriteBack);
    let wbInst = wb_ir;
    
    rf.wr(validRegValue(wbInst.dst), wbInst.data);
    
    pc <= wbInst.brTaken ? wbInst.addr : pc + 4;
    
    cop.wr(wbInst.dst, wbInst.data);
    
    state <= Fetch;
  endrule
  
  method ActionValue#(Tuple2#(RIndx, Data)) cpuToHost;
    let ret <- cop.cpuToHost;
    return ret;
  endmethod

  method Action hostToCpu(Bit#(32) startpc) if (!cop.started);
    cop.start;
    pc <= startpc;
  endmethod
endmodule

//comment
// Minimal change from the 1-cycle implementation : Only ir and state were introduced
// The fetch and execute rules are mutually exclusive
// Princeton architecture doesn't add any complication to the Harvard architecture used in this example because the memory ports are accessed serially
