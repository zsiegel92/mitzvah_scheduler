import { Injectable } from '@angular/core';
import { DoubleDate } from './DoubleDate';
import { School } from './school';

@Injectable()
export class FormService {
	public birthday: DoubleDate;
	public entry: {email: string, childName: string, school: string,schoolId:number,  hebSchool: string,hebSchoolId:number,DOB: Date} = {email: '', childName: '', school: '',schoolId:-1,  hebSchool: '',hebSchoolId:-1,DOB: null};


	set_email(email:string){
		this.entry.email=email;
	}


	avoid_days: DoubleDate[];

  constructor() {


  }

}
