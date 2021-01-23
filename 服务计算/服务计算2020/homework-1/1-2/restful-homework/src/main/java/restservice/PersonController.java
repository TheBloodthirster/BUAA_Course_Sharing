package restservice;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class PersonController {
    Map<Long, Person> personMap;

    PersonController() {
        this.personMap = new HashMap<Long, Person>();
    }

    @GetMapping("/people")
    public List<Person> getPeople() {
        return new ArrayList<>(personMap.values());
    }

    @GetMapping("/people/{id}")
    public Person getPerson(@PathVariable Long id) {
        return personMap.get(id);
    }

    @PostMapping("/people")
    public Person postPerson(@RequestBody Person person) {
        personMap.put(person.getId(), person);
        return person;
    }

    @PutMapping("/people/{id}")
    public Person putPerson(@PathVariable Long id, @RequestBody Person person) {
        personMap.put(id, person);
        return person;
    }
    @DeleteMapping("/people/{id}")
    public void deletePerson(@PathVariable Long id) {
        personMap.remove(id);
    }

}
