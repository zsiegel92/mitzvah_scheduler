import { Component, OnInit, ViewChild } from '@angular/core';
// import {NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';

import { DataService } from '../data.service';
import { School } from '../school';

import { FormStudentComponent } from '../form-student/form-student.component';
import { FormVenueComponent } from '../form-venue/form-venue.component';
import { FormDateComponent } from '../form-date/form-date.component';
import { FormAccommodationComponent } from '../form-accommodation/form-accommodation.component';

import { SchoolSelectorComponent } from '../school-selector/school-selector.component';
import { DatepickerComponent } from '../datepicker/datepicker.component';
import { FormService } from '../form.service';

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.css']
})
export class FormComponent implements OnInit {
		@ViewChild("studentform") studentForm: FormStudentComponent;
		@ViewChild("venueform") venueForm: FormVenueComponent;
		@ViewChild("dateform") dateForm: FormDateComponent;
		@ViewChild("accommodationform") accommodationForm: FormAccommodationComponent;

		comps: any[];

		schools: School[];
		step: number;


	getSchools(): void {
	  this.dataService.getSchools()
	      .subscribe(schools => this.schools = schools);
	}

	// back():void{
	// 	this.syncForm();
	// 	if (this.step > 0){
	// 		this.step--;
	// 	}
	// 	this.prepForm();
	// }
	// forward():void{
	// 	this.syncForm();
	// 	if (this.step < 3){
	// 		this.step++;
	// 	}
	// 	this.prepForm();
	// }
	move(steps:number):void{
		this.syncForm();
		if ((this.step + steps > -1) && (this.step + steps < 4)){
			this.step = this.step + steps;
		}
		this.prepForm();
	}
	syncForm(){
		this.comps[this.step].syncForm();
	}

	prepForm(){
		this.comps[this.step].prepForm();
	}

  constructor(private dataService: DataService,private formService: FormService) {
  	this.step=0;
  }

  ngOnInit() {
  	this.comps = [this.studentForm,this.venueForm,this.dateForm,this.accommodationForm];
  	this.getSchools();
  }

}
