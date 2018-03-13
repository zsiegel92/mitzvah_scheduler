import {Component, Input, OnInit, ViewChild} from '@angular/core';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { DoubleDate } from '../DoubleDate';

// import { DatepickerComponent } from '../datepicker/datepicker.component';
import { FormService } from '../form.service';
// import { DoubleDate } from '../DoubleDate';

const now = new Date();

@Component({
  selector: 'app-form-date',
  templateUrl: './form-date.component.html',
  styleUrls: ['./form-date.component.css']
})
export class FormDateComponent implements OnInit {


	birthday: NgbDateStruct = {year: now.getFullYear(), month: now.getMonth() + 1, day: now.getDate()};
	models: DoubleDate[];
	maxDate: NgbDateStruct;
	minDate: NgbDateStruct;
	have_birthday: boolean = false;

	push_date() {
	  this.models.push(new DoubleDate());
	}

	pop_date(i: number) {
	  this.models.splice(i,1);
	}

	setBirthday(bd: NgbDateStruct){
	  this.have_birthday = true;
	  this.birthday = bd;
	}

	sync(a_dp_component,greg: NgbDateStruct){
	  a_dp_component.navigateTo({ year: greg.year, month: greg.month });
	}

	isNotSaturday(a_date: NgbDateStruct) {
	    const d = new Date(a_date.year, a_date.month - 1, a_date.day);
	    return d.getDay() !== 6;
	  }

	syncForm(){

	}
	prepForm(){
		// this.birthday=this.formService.birthday.getGreg();
		this.setBirthday(this.formService.birthday.getGreg());

	}


  constructor(private formService: FormService) {
  	this.maxDate = {year: now.getFullYear() + 1, month: now.getMonth() + 1, day: now.getDate()};
  	this.minDate = {year: now.getFullYear() - 15, month: now.getMonth() + 1, day: now.getDate()};
  }

  ngOnInit() {
  	this.models=[];
  }

}
