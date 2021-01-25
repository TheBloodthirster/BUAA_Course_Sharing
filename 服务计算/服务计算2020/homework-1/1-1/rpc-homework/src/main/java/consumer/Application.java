package consumer;


import api.PersonService;
import org.apache.dubbo.config.ApplicationConfig;
import org.apache.dubbo.config.ReferenceConfig;
import org.apache.dubbo.config.RegistryConfig;

public class Application {
    private static String zookeeperHost = System.getProperty("zookeeper.address", "127.0.0.1");

    public static void main(String[] args) {
        ReferenceConfig<PersonService> reference = new ReferenceConfig<>();
        reference.setApplication(new ApplicationConfig("first-dubbo-consumer"));
        reference.setRegistry(new RegistryConfig("zookeeper://" + zookeeperHost + ":2181"));
        reference.setInterface(PersonService.class);
        PersonService service = reference.get();

        service.setName("admin");
        service.setAge(18);
        service.setGender(false);
        System.out.println(service.sayHello());
        System.out.println(service.getAge());
        System.out.println(service.getGender()?"male":"female");
    }
}