import { Component, OnInit, ViewChild } from '@angular/core';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule,NgForm } from '@angular/forms';

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
	@ViewChild("f") f: NgForm;

	schools: School[];
	hebSchools: School[];
	all_schools: {schools: School[], hebSchools: School[]};
	selectedSchool: School;
	selectedHebSchool: School;
	otherSchool: School;
	otherHebSchool: School;



	model: DoubleDate;
	maxDate: NgbDateStruct;
	minDate: NgbDateStruct;


	get_all_schools(){
		this.all_schools = this.formService.all_schools;
	}
	syncForm(){
		this.formService.birthday=this.model;
		this.formService.entry.school = this.selectedSchool.name;
		this.formService.entry.schoolId = this.selectedSchool.id;
		this.formService.entry.hebSchool = this.selectedHebSchool.name;
		this.formService.entry.hebSchoolId = this.selectedHebSchool.id;
		this.formService.entry.DOB = this.model.hgregorian;
	}


	prepForm(){

	}

  constructor(public formService: FormService,private dataService: DataService) {
    this.maxDate = {year: now.getFullYear() + 1, month: now.getMonth() + 1, day: now.getDate()};
  	this.minDate = {year: now.getFullYear() - 15, month: now.getMonth() + 1, day: now.getDate()};
  	this.otherSchool = new School();
  	this.otherHebSchool = new School();
  	this.selectedSchool= this.otherSchool;
  	this.selectedHebSchool = this.otherHebSchool;
  }

  ngOnInit() {
  	this.model = new DoubleDate();
  	this.model.thirteen_ago();
  	this.get_all_schools();
  }

}
