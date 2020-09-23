package com.faraz.portfolio.dao;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.faraz.portfolio.models.Contact;

public interface ContactRepository extends JpaRepository<Contact, Long>{
	
	List<Contact> findByName(String Name);
	List<Contact> findByContactType(String ContactType);
	
}
