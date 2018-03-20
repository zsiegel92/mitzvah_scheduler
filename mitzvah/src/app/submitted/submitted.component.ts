import { Component, OnInit } from '@angular/core';
import { NotFoundComponent } from '../not-found/not-found.component';
import { FormService } from '../form.service';
import { DataService } from '../data.service';

@Component({
  selector: 'app-submitted',
  templateUrl: './submitted.component.html',
  styleUrls: ['./submitted.component.css']
})
export class SubmittedComponent implements OnInit {
	// entry: any;
	Object = Object; //to use Object.keys(my_obj)

  constructor(public formService: FormService,private dataService: DataService) {

  }

  ngOnInit() {
  	// this.entry = this.formService.entry;
  }

}
