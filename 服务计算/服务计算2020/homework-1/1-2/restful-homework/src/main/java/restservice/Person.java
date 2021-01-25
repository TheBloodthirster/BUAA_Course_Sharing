package restservice;



public class Person  {
    private Long id;
    private String name;
    private int age;
    private boolean gender;

    public Person(){}
    public Person(Long id) {
        this.id = id;
    }


    public String sayHello() {
        return "Hello world !" + name;
    }


    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public boolean getGender() {
        return gender;
    }

    public void setGender(boolean gender) {
        this.gender = gender;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Long getId() {
        return id;
    }
}
