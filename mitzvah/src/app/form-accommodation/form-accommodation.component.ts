import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FormService } from '../form.service';

@Component({
  selector: 'app-form-accommodation',
  templateUrl: './form-accommodation.component.html',
  styleUrls: ['./form-accommodation.component.css']
})
export class FormAccommodationComponent implements OnInit {
	accommodation: boolean = false;
	accommodation_other: string = '';
	twin: boolean = false;

	syncForm(){
		this.formService.entry.accommodation = this.accommodation;
		this.formService.entry.accommodation_other = this.accommodation_other;
		this.formService.entry.twin = this.twin;
	}
	prepForm(){

	}

  constructor(private formService: FormService) { }

  ngOnInit() {
  }

}
