import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-form-accommodation',
  templateUrl: './form-accommodation.component.html',
  styleUrls: ['./form-accommodation.component.css']
})
export class FormAccommodationComponent implements OnInit {
	accommodation: boolean = false;
	twin: boolean = false;
  constructor() { }

  ngOnInit() {
  }

}
