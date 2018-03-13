import { Component, OnInit, ViewChild } from '@angular/core';
// import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { DatepickerComponent } from '../datepicker/datepicker.component';
import { FormService } from '../form.service';
// import { DoubleDate } from '../DoubleDate';

@Component({
  selector: 'app-form-date',
  templateUrl: './form-date.component.html',
  styleUrls: ['./form-date.component.css']
})
export class FormDateComponent implements OnInit {

	@ViewChild("dp") dp: DatepickerComponent;


	// birthday: NgbDateStruct;

	syncForm(){

	}
	prepForm(){
		// this.birthday=this.formService.birthday.getGreg();
		this.dp.setBirthday(this.formService.birthday.getGreg());

	}

  constructor(private formService: FormService) {
  }

  ngOnInit() {
  }

}
