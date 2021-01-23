package axis2;

import java.rmi.RemoteException;

import org.apache.axis2.AxisFault;

public class Test {
 public static void main(String args[]) throws RemoteException {
	 MyService myService=new MyServiceStub();
	 SetName setName=new SetName();
	 setName.setName("admin");
	 myService.setName(setName);
	 SayHelloResponse sayHelloResponse=myService.sayHello(new SayHello());
	 System.out.println(sayHelloResponse.get_return());  
 }
}
