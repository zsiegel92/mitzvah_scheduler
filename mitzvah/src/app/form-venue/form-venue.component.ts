import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FormService } from '../form.service';

@Component({
  selector: 'app-form-venue',
  templateUrl: './form-venue.component.html',
  styleUrls: ['./form-venue.component.css']
})
export class FormVenueComponent implements OnInit {
	// model = {main: 0, family_minyan: 0, torah_round: 0}
	models = [{name:"Main Sanctuary",value: 0,id:0},{name:"Family Minyan",value: 0,id:1},{name:"Torah In The Round",value: 0,id:2}];

	syncForm(){
		this.formService.entry.rankings=this.models;
	}
	prepForm(){

	}

  constructor(private formService: FormService) { }

  ngOnInit() {
  	this.formService.entry.rankings=this.models;
  }

}
