
/**
 * MyServiceCallbackHandler.java
 *
 * This file was auto-generated from WSDL
 * by the Apache Axis2 version: 1.7.9  Built on : Nov 16, 2018 (12:05:37 GMT)
 */

    package axis2;

    /**
     *  MyServiceCallbackHandler Callback class, Users can extend this class and implement
     *  their own receiveResult and receiveError methods.
     */
    public abstract class MyServiceCallbackHandler{



    protected Object clientData;

    /**
    * User can pass in any object that needs to be accessed once the NonBlocking
    * Web service call is finished and appropriate method of this CallBack is called.
    * @param clientData Object mechanism by which the user can pass in user data
    * that will be avilable at the time this callback is called.
    */
    public MyServiceCallbackHandler(Object clientData){
        this.clientData = clientData;
    }

    /**
    * Please use this constructor if you don't want to set any clientData
    */
    public MyServiceCallbackHandler(){
        this.clientData = null;
    }

    /**
     * Get the client data
     */

     public Object getClientData() {
        return clientData;
     }

        
               // No methods generated for meps other than in-out
                
               // No methods generated for meps other than in-out
                
           /**
            * auto generated Axis2 call back method for getAge method
            * override this method for handling normal response from getAge operation
            */
           public void receiveResultgetAge(
                    axis2.GetAgeResponse result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from getAge operation
           */
            public void receiveErrorgetAge(java.lang.Exception e) {
            }
                
           /**
            * auto generated Axis2 call back method for sayHello method
            * override this method for handling normal response from sayHello operation
            */
           public void receiveResultsayHello(
                    axis2.SayHelloResponse result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from sayHello operation
           */
            public void receiveErrorsayHello(java.lang.Exception e) {
            }
                
           /**
            * auto generated Axis2 call back method for getName method
            * override this method for handling normal response from getName operation
            */
           public void receiveResultgetName(
                    axis2.GetNameResponse result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from getName operation
           */
            public void receiveErrorgetName(java.lang.Exception e) {
            }
                
           /**
            * auto generated Axis2 call back method for isGender method
            * override this method for handling normal response from isGender operation
            */
           public void receiveResultisGender(
                    axis2.IsGenderResponse result
                        ) {
           }

          /**
           * auto generated Axis2 Error handler
           * override this method for handling error response from isGender operation
           */
            public void receiveErrorisGender(java.lang.Exception e) {
            }
                
               // No methods generated for meps other than in-out
                


    }
    