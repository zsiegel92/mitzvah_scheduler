import { Component, OnInit, ViewChild } from '@angular/core';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { DoubleDate } from '../DoubleDate';

// import { DatepickerComponent } from '../datepicker/datepicker.component';
import { FormService } from '../form.service';

const now = new Date();

@Component({
  selector: 'app-form-student',
  templateUrl: './form-student.component.html',
  styleUrls: ['./form-student.component.css']
})
export class FormStudentComponent implements OnInit {


	model: DoubleDate;

	maxDate: NgbDateStruct;
	minDate: NgbDateStruct;

	syncForm(){
		this.formService.birthday=this.model;
	}
	prepForm(){

	}

  constructor(private formService: FormService) {
  	this.maxDate = {year: now.getFullYear() + 1, month: now.getMonth() + 1, day: now.getDate()};
  	this.minDate = {year: now.getFullYear() - 15, month: now.getMonth() + 1, day: now.getDate()};
  }

  ngOnInit() {
  	this.model = new DoubleDate();
  }

}
