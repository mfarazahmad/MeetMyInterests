package com.faraz.portfolio.dao;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.faraz.portfolio.models.Blog;

public interface BlogRepository extends JpaRepository<Blog, Long>{
	
	List<Blog> findByAuthor(String Author);

}
