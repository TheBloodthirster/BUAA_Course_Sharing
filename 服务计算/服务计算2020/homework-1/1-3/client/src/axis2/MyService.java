

/**
 * MyService.java
 *
 * This file was auto-generated from WSDL
 * by the Apache Axis2 version: 1.7.9  Built on : Nov 16, 2018 (12:05:37 GMT)
 */

    package axis2;

    /*
     *  MyService java interface
     */

    public interface MyService {
          
       /**
         * Auto generated method signature for Asynchronous Invocations
         * 
         */
        public void  setName(
         axis2.SetName setName0

        ) throws java.rmi.RemoteException
        
        ;

        
       /**
         * Auto generated method signature for Asynchronous Invocations
         * 
         */
        public void  setGender(
         axis2.SetGender setGender1

        ) throws java.rmi.RemoteException
        
        ;

        

        /**
          * Auto generated method signature
          * 
                    * @param getAge2
                
         */

         
                     public axis2.GetAgeResponse getAge(

                        axis2.GetAge getAge2)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param getAge2
            
          */
        public void startgetAge(

            axis2.GetAge getAge2,

            final axis2.MyServiceCallbackHandler callback)

            throws java.rmi.RemoteException;

     

        /**
          * Auto generated method signature
          * 
                    * @param sayHello4
                
         */

         
                     public axis2.SayHelloResponse sayHello(

                        axis2.SayHello sayHello4)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param sayHello4
            
          */
        public void startsayHello(

            axis2.SayHello sayHello4,

            final axis2.MyServiceCallbackHandler callback)

            throws java.rmi.RemoteException;

     

        /**
          * Auto generated method signature
          * 
                    * @param getName6
                
         */

         
                     public axis2.GetNameResponse getName(

                        axis2.GetName getName6)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param getName6
            
          */
        public void startgetName(

            axis2.GetName getName6,

            final axis2.MyServiceCallbackHandler callback)

            throws java.rmi.RemoteException;

     

        /**
          * Auto generated method signature
          * 
                    * @param isGender8
                
         */

         
                     public axis2.IsGenderResponse isGender(

                        axis2.IsGender isGender8)
                        throws java.rmi.RemoteException
             ;

        
         /**
            * Auto generated method signature for Asynchronous Invocations
            * 
                * @param isGender8
            
          */
        public void startisGender(

            axis2.IsGender isGender8,

            final axis2.MyServiceCallbackHandler callback)

            throws java.rmi.RemoteException;

     
       /**
         * Auto generated method signature for Asynchronous Invocations
         * 
         */
        public void  setAge(
         axis2.SetAge setAge10

        ) throws java.rmi.RemoteException
        
        ;

        

        
       //
       }
    