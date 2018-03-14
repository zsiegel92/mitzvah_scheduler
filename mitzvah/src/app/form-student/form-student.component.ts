import { Component, OnInit, ViewChild } from '@angular/core';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { DoubleDate } from '../DoubleDate';

import { School } from '../school';

import { DataService } from '../data.service';
import { FormService } from '../form.service';

const now = new Date();

@Component({
  selector: 'app-form-student',
  templateUrl: './form-student.component.html',
  styleUrls: ['./form-student.component.css']
})
export class FormStudentComponent implements OnInit {

	schools: School[];
	hebSchools: School[];
	selectedSchool: School;
	selectedHebSchool: School;
	otherSchool: School;
	otherHebSchool: School;

	model: DoubleDate;

	maxDate: NgbDateStruct;
	minDate: NgbDateStruct;

	getSchools(): void {
	  this.dataService.getSchools()
	      .subscribe(schs => this.schools = schs);
	}

	getHebSchools(): void {
	  this.dataService.getHebSchools()
	      .subscribe(schs => this.hebSchools = schs);
	}

	syncForm(){
		this.formService.birthday=this.model;
	}
	prepForm(){
	}

  constructor(private formService: FormService,private dataService: DataService) {
  	this.maxDate = {year: now.getFullYear() + 1, month: now.getMonth() + 1, day: now.getDate()};
  	this.minDate = {year: now.getFullYear() - 15, month: now.getMonth() + 1, day: now.getDate()};
  	this.otherSchool = new School();
  	this.otherHebSchool = new School();
  	this.selectedSchool= this.otherSchool;
  	this.selectedHebSchool = this.otherHebSchool;
  }

  ngOnInit() {
  	this.model = new DoubleDate();
  	this.getSchools();
  	// this.schools=[];
  	this.getHebSchools();
  }

}
