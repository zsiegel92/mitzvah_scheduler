import { Component, OnInit } from '@angular/core';
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

		schools: School[];
		step: number;


	getSchools(): void {
	  this.dataService.getSchools()
	      .subscribe(schools => this.schools = schools);
	}

	back():void{
		if (this.step > 1){
			this.step--;
		}
	}
	forward():void{
		if (this.step < 4){
			this.step++;
		}
	}

  constructor(private dataService: DataService,private formService: FormService) {
  	this.step=1;
  }

  ngOnInit() {
  	this.getSchools();
  }

}
