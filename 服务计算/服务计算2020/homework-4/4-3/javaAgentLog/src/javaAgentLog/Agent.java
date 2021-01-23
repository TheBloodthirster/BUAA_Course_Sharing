package javaAgentLog;

import javassist.CannotCompileException;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtMethod;

import java.lang.instrument.Instrumentation;

public class Agent {
    private static String systemPrint(String prefix, String methodName) {
        return "System.out.println(\"__" + prefix + "__ " + methodName + ": \" + System.nanoTime() + \" \" + Thread.currentThread().getId());";
    }

    public static void premain(String agentArgs, Instrumentation inst) {
        ClassPool cp = ClassPool.getDefault();
        inst.addTransformer((classLoader, s, aClass, protectionDomain, bytes) -> {
            if (s.startsWith("org/apache/hadoop")) {
                try {
                    CtClass cc = cp.get(s.replace('/', '.'));
                    for (CtMethod m : cc.getDeclaredMethods()) {
                        try {
                            m.insertBefore(systemPrint("enter", cc.getName() + " " + m.getName()));
                            m.insertAfter(systemPrint("exit", cc.getName() + " " + m.getName()));
                        }catch (CannotCompileException ignored){}
                    }
                    byte[] byteCode = cc.toBytecode();
                    cc.detach();
                    return byteCode;
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }
            return bytes;
        });
    }
}

