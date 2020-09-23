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

import com.faraz.portfolio.dao.BlogRepository;
import com.faraz.portfolio.models.Blog;

@RestController
@RequestMapping("/blog")
public class BlogController {
	
	@Autowired
	BlogRepository repository;
	
	@GetMapping("/")
	public List<Blog> getAllBlogs() {
		return repository.findAll();
	}
	
	@GetMapping("/{id}")
	public Optional<Blog> getBlog(@PathVariable int id) {
		return repository.findById((long) id);
	}
	
	@GetMapping("/{author}")
	public List<Blog> getBlogByAuthor(@PathVariable String author) {
		return repository.findByAuthor(author);
	}
	
	@PostMapping("/")
	public Blog saveBlog(@RequestBody Blog newBlog) {
		return repository.save(newBlog);
	}
	
	@PutMapping("/")
	public Blog updateBlog(@RequestBody Blog updatedBlog) {
		return repository.save(updatedBlog);
	}

	@DeleteMapping("/{id}")
	public void deleteBlog(@PathVariable int id) {
		repository.deleteById((long) id);
	}


}
