import { Component, OnInit, ViewChild } from '@angular/core';
import { FormsModule,NgForm } from '@angular/forms';
import { FormService } from '../form.service';

@Component({
  selector: 'app-form-accommodation',
  templateUrl: './form-accommodation.component.html',
  styleUrls: ['./form-accommodation.component.css']
})
export class FormAccommodationComponent implements OnInit {
	@ViewChild("f") f: NgForm;
	accommodation: boolean = true;
	accommodation_other: string = "";
	twin: boolean = false;

	syncForm(){
		this.formService.entry.accommodation = this.accommodation;
		this.formService.entry.accommodation_other = this.accommodation_other;
		this.formService.entry.twin = this.twin;
	}
	prepForm(){

	}

  constructor(private formService: FormService) {
  	this.accommodation = true;
  }

  ngOnInit() {
  }

}
