package com.faraz.portfolio.models;

import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import lombok.Data;

@Entity
@Table (name = "BLOG")
@Data
public class Blog {
	
	@Id
	@Column
	@GeneratedValue
	private int id;
	
	@Column
	private String tags;
	
	@Column
	private String title;
	
	@Column
	private String content;
	
	@Column
	private String images;
	
	@Column
	private String author;
	
	@Column
	@CreationTimestamp
	private Date createdOn;
	
	@Column
	@UpdateTimestamp
	private Date modifiedOn;
}
