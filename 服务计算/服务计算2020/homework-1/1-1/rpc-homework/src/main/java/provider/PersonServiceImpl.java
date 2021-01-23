package provider;

import api.PersonService;

public class PersonServiceImpl implements PersonService {
    private String name;
    private int age;
    private boolean gender;


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
}