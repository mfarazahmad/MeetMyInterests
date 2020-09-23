package com.faraz.portfolio.dao;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.faraz.portfolio.models.Comments;

public interface CommentRepository extends JpaRepository<Comments, Long>{

	List<Comments> findByName(String Name);
}
