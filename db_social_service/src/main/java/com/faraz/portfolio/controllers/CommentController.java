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

import com.faraz.portfolio.dao.CommentRepository;
import com.faraz.portfolio.models.Comments;

@RestController
@RequestMapping("/comment")
public class CommentController {
	
	@Autowired
	CommentRepository repository;
	
	@GetMapping("/")
	public List<Comments> getAllComments() {
		return repository.findAll();
	}
	
	@GetMapping("/{id}")
	public Optional<Comments> getComment(@PathVariable int id) {
		return repository.findById((long) id);
	}
	
	@GetMapping("/{name}")
	public List<Comments> getCommentByName(@PathVariable String name) {
		return repository.findByName(name);
	}
	
	
	@PostMapping("/")
	public Comments saveComment(@RequestBody Comments newComment) {
		return repository.save(newComment);
	}
	
	@PutMapping("/")
	public Comments updateComment(@RequestBody Comments updatedComment) {
		return repository.save(updatedComment);
	}

	@DeleteMapping("/{id}")
	public void deleteComment(@PathVariable int id) {
		repository.deleteById((long) id);
	}


}
