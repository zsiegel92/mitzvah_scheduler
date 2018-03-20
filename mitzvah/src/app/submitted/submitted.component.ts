import { Component, OnInit } from '@angular/core';
import { NotFoundComponent } from '../not-found/not-found.component';
import { FormService } from '../form.service';

@Component({
  selector: 'app-submitted',
  templateUrl: './submitted.component.html',
  styleUrls: ['./submitted.component.css']
})
export class SubmittedComponent implements OnInit {
	// entry: any;
	Object = Object;

  constructor(public formService: FormService) { }

  ngOnInit() {
  	// this.entry = this.formService.entry;
  }

}
