import { Component, OnInit, ViewChild } from '@angular/core';
// import {NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';

import { DataService } from '../data.service';

import { FormStudentComponent } from '../form-student/form-student.component';
import { FormVenueComponent } from '../form-venue/form-venue.component';
import { FormDateComponent } from '../form-date/form-date.component';
import { FormAccommodationComponent } from '../form-accommodation/form-accommodation.component';

import { SchoolSelectorComponent } from '../school-selector/school-selector.component';
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

		step: number;
		comp;


	move(steps:number):void{
		this.comp.syncForm();
		if ((this.step + steps > -1) && (this.step + steps < 4)){
			this.step = this.step + steps;
		}
		this.setcomp()
		this.comp.prepForm();
	}

	invalidform(){
		return false
	}

	setcomp(){
		this.comp = this.comps[this.step];
	}

  constructor(private dataService: DataService,private formService: FormService) {
  	this.step=0;
  }

  ngOnInit() {
  	this.comps = [this.studentForm,this.venueForm,this.dateForm,this.accommodationForm];
  	this.setcomp();
  }

}
