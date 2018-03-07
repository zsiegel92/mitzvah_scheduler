import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { School } from '../school';

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.css']
})
export class FormComponent implements OnInit {
	schools: School[];
	// schools = SCHOOLS;

	// getSchools(): void {
	//   this.schools = this.dataService.getSchools();
	// }

	getSchools(): void {
	  this.dataService.getSchools()
	      .subscribe(schools => this.schools = schools);
	}


	// submitted = false;

	// onSubmit() { this.submitted = true; }


  constructor(private dataService: DataService) { }

  ngOnInit() {
  	this.getSchools();
  }

}
