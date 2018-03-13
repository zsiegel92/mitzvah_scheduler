import { Component, OnInit, ViewChild } from '@angular/core';
import { DatepickerComponent } from '../datepicker/datepicker.component';
import { FormService } from '../form.service';


@Component({
  selector: 'app-form-student',
  templateUrl: './form-student.component.html',
  styleUrls: ['./form-student.component.css']
})
export class FormStudentComponent implements OnInit {
	@ViewChild("dp") dp: DatepickerComponent;

	syncForm(){
		this.formService.birthday=this.dp.getModels()[0];
	}
	prepForm(){

	}

  constructor(private formService: FormService) {}

  ngOnInit() {
  }

}
