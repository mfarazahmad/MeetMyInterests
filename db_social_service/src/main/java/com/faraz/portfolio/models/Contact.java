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
@Table (name = "CONTACT")
@Data
public class Contact {
	
	@Id
	@Column
	@GeneratedValue
	private int id;
	
	@Column
	private String name;
	
	@Column
	private String requestType;
	
	@Column
	private String contactType;
	
	@Column
	private String contact;
	
	@Column
	private String bestTime;
	
	@Column
	private String message;
	
	@Column
	@CreationTimestamp
	private Date createdOn;
	
}
