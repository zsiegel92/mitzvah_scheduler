import { Component, OnInit } from '@angular/core';
// import {NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';

import { DataService } from '../data.service';
import { School } from '../school';
import { SchoolSelectorComponent } from '../school-selector/school-selector.component';
import { DatepickerComponent } from '../datepicker/datepicker.component';


@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.css']
})
export class FormComponent implements OnInit {

	// dateStructs: NgbDateStruct[] =[];



	schools: School[];

	getSchools(): void {
	  this.dataService.getSchools()
	      .subscribe(schools => this.schools = schools);
	}

	// pushDate(): void {
	// 	this.dateStructs.push()
	// }
	// submitted = false;

	// onSubmit() { this.submitted = true; }


  constructor(private dataService: DataService) { }

  ngOnInit() {
  	this.getSchools();
  }

}
