/*

Copyright (C) 2012 Muralidaran Vijayaraghavan <vmurali@csail.mit.edu>

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
import Fifo::*;
import AddrPred::*;
import Scoreboard::*;

typedef struct {
  Addr pc;
  Addr ppc;
  Data inst;
  Bool epoch;
} Fetch2Execute deriving (Bits, Eq);

// 加入计分板后需要创建新的结构体

typedef struct {
  Addr pc;
  Addr ppc;
  Data inst;
  Bool epoch;
  DecodedInst dInst;
  Data rVal1;
  Data rVal2;
} NewFetch2Execute deriving (Bits, Eq);

typedef struct {
  Maybe#(FullIndx) dst;
  Data data;
} NewExecute2WriteBack deriving (Bits, Eq);


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
  AddrPred pcPred <- mkBtb;

  //Fifo#(1, Fetch2Execute) ir <- mkPipelineFifo;
  //Fifo#(2, Fetch2Execute) ir <- mkCFFifo;
  // 创建新的队列，注意类型要改为mkPipelineFifo
  Fifo#(2, NewFetch2Execute) ifr <- mkPipelineFifo;
  Fifo#(2, NewExecute2WriteBack) iwr <- mkPipelineFifo;
  Fifo#(1, Redirect) execRedirect <- mkBypassFifo;
  //Fifo#(2, Redirect)   execRedirect <- mkCFFifo;
  
  // 再加入一个计分板类型存储值
  Scoreboard#(2) sb <- mkCFScoreboard;
  
  //This design uses two epoch registers, one for each stage of the pipeline. Execute sets the eEpoch and discards any instruction that doesn't match it. It passes the information about change of epoch to fetch stage indirectly by passing a valid execRedirect using a Fifo. Fetch changes fEpoch everytime it gets a execRedirect and tags every instruction with its epoch

  Reg#(Bool) fEpoch <- mkReg(False);
  Reg#(Bool) eEpoch <- mkReg(False);

  // 按照实验要求，取值阶段需要完成Fetch, Decode, Register Read三个任务
  rule doFetch(cop.started);
    let inst = iMem.req(pc);

    $display("Fetch: pc: %h inst: (%h) expanded: ", pc, inst, showInst(inst));
    
    // 取值完成后，需要Decode，并且记录计分板的值
    let dInst = decode(inst);
    let socreboard_flag = sb.search2(dInst.src1) || sb.search2(dInst.src2);

    
    // dequeue the incoming redirect and update the predictor whether it's a mispredict or not
    // 使传入的重定向出队并更新预测变量，无论它是否有误预测
    if(execRedirect.notEmpty)
    begin
      execRedirect.deq;
      pcPred.update(execRedirect.first);
    end
    // change pc and the fetch's copy of the epoch only on a mispredict
    // 仅在错误预测下更改pc和epoch的获取副本
    if(execRedirect.notEmpty && execRedirect.first.mispredict)
    begin
      fEpoch <= !fEpoch;
      pc <= execRedirect.first.nextPc;
    end
    // fetch the new instruction on a non mispredict
    // 预测错误的话重写取指过程 
    else
    begin
      if(!socreboard_flag)
        begin
        
          let ppc = pcPred.predPc(pc);
          pc <= ppc;
          let rVal1 = rf.rd1(validRegValue(dInst.src1));
          let rVal2 = rf.rd2(validRegValue(dInst.src2));
		  // 传到执行阶段用于第三阶段流水
          ifr.enq(NewFetch2Execute{pc:pc , ppc:ppc , inst:inst , epoch:fEpoch , dInst:dInst , rVal1:rVal1 , rVal2: rVal2});
          sb.insert(dInst.dst);
          
          //ir.enq(Fetch2Execute{pc: pc, ppc: ppc, inst: inst, epoch: fEpoch});
        end
    end
  endrule

  // 执行阶段需要完成Execute, Memory两个任务
  rule doExecute;
    let inst  = ifr.first.inst;
    let pc    = ifr.first.pc;
    let ppc   = ifr.first.ppc;
    let epoch = ifr.first.epoch;

    // Proceed only if the epochs match
    if(epoch == eEpoch)
    begin
      $display("Execute: pc: %h inst: (%h) expanded: ", pc, inst, showInst(inst));
      
      // 已经移动到前面Fetch，没用注释掉
      // let dInst = decode(inst);
      // let rVal1 = rf.rd1(validRegValue(dInst.src1));
      // let rVal2 = rf.rd2(validRegValue(dInst.src2));
      
      let dInst = ifr.first.dInst;
      let rVal1 = ifr.first.rVal1;
      let rVal2 = ifr.first.rVal2;
  
      let copVal = cop.rd(validRegValue(dInst.src1));
  
      let eInst = exec(dInst, rVal1, rVal2, pc, ppc, copVal);
  
      if(eInst.iType == Unsupported)
      begin
        $fwrite(stderr, "Executing unsupported instruction at pc: %x. Exiting\n", pc);
        $finish;
      end

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

      if (isValid(eInst.dst) && validValue(eInst.dst).regType == Normal)
        // 写回移动到写回阶段执行代码，并且为了数据转
        //rf.wr(validRegValue(eInst.dst), eInst.data);
        iwr.enq(NewExecute2WriteBack{dst:eInst.dst , data:eInst.data});
        sb.remove;
                  
  
        // Send the branch resolution to fetch stage, irrespective of whether it's mispredicted or not
        // TBD: put code here that does what the comment immediately above says
        // 将分支解决方案发送到访存阶段，无论它是否被错误预测
      if(eInst.brTaken)
        begin
          execRedirect.enq(Redirect{nextPc: eInst.addr,mispredict:eInst.mispredict});
        end
        // On a branch mispredict, change the epoch, to throw away wrong path instructions
        // TBD: put code here that does what the comment immediately above says
        // 在分支预测错误的情况下，更改epoch以丢弃错误的路径指令
      if(eInst.brTaken && eInst.mispredict)
        begin
          eEpoch <= !eEpoch;
        end 
      cop.wr(eInst.dst, eInst.data);
    end
    else
      // 预测错误，清空计分板
      sb.remove;
      
    ifr.deq;
  endrule
  
  // 写回阶段
  rule doWriteBack;
    let dst = iwr.first.dst;
    let data = iwr.first.data;
    rf.wr(validRegValue(dst), data);
    iwr.deq();
    sb.remove;
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

//comments
// This code also works with either (or both) Fifo replaced with CFFifo
// If both Fifos are CFFifo, then fetch and execute are also conflict free
// If either Fifo is not CFFifo, then fetch and execute can be scheduled concurrently, with execute<fetch
// If BypassFifo is used for pc-redirect, then the processor is slightly faster
// This is by far the most robust solution as we will see later
