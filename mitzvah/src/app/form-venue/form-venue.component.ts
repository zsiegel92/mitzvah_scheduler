import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FormService } from '../form.service';

@Component({
  selector: 'app-form-venue',
  templateUrl: './form-venue.component.html',
  styleUrls: ['./form-venue.component.css']
})
export class FormVenueComponent implements OnInit {
	model1 = 0;
	model2 = 0;
	model3 = 0;

	syncForm(){

	}
	prepForm(){

	}

  constructor() { }

  ngOnInit() {
  }

}