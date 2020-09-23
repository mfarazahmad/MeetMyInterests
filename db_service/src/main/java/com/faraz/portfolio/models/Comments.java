package com.faraz.portfolio.models;

import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import org.hibernate.annotations.CreationTimestamp;

import lombok.Data;

@Entity
@Table  (name = "COMMENTS")
@Data
public class Comments {
	
	@Id
	@Column
	@GeneratedValue
	private int id;
	
	@Column
	private String name;
	
	@Column
	private String userComment;
	
	@Column
	@CreationTimestamp
	private Date createdOn;
	
}
