package axis2;

public class person  {
    private static String name;
    private static int age;
    private static boolean gender;

    public person(){}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}

	public boolean isGender() {
		return gender;
	}

	public void setGender(boolean gender) {
		this.gender = gender;
	}

    public String sayHello() {
        return "Hello world !" + name;
    }


}
