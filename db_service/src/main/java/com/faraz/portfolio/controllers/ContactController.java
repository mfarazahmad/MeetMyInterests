package com.faraz.portfolio.controllers;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.faraz.portfolio.dao.ContactRepository;
import com.faraz.portfolio.models.Contact;

@RestController
@RequestMapping("/contact")
public class ContactController {
	
	@Autowired
	ContactRepository repository;
	
	@GetMapping("/")
	public List<Contact> getAllContacts() {
		return repository.findAll();
	}
	
	@GetMapping("/{id}")
	public Optional<Contact> getContact(@PathVariable int id) {
		return repository.findById((long) id);
	}
	
	@GetMapping("/{name}")
	public List<Contact> getContactByName(@PathVariable String name) {
		return repository.findByName(name);
	}
	
	@GetMapping("/type/{contactType}")
	public List<Contact> getContactByType(@PathVariable String contactType) {
		return repository.findByContactType(contactType);
	}
	
	@PostMapping("/")
	public Contact saveContact(@RequestBody Contact newContact) {
		return repository.save(newContact);
	}
	
	@PutMapping("/")
	public Contact updateContact(@RequestBody Contact updatedContact) {
		return repository.save(updatedContact);
	}

	@DeleteMapping("/{id}")
	public void deleteContact(@PathVariable int id) {
		repository.deleteById((long) id);
	}


}
