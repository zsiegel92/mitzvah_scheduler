import { Injectable } from '@angular/core';
import { DoubleDate } from './DoubleDate';
import { School } from './school';

@Injectable()
export class FormService {
	public birthday: DoubleDate;
	public entry: {email: string, childName: string, school: string,schoolId:number,  hebSchool: string,hebSchoolId:number,DOB: Date, rankings: any[],nonDates: DoubleDate[],accommodation: boolean,accommodation_other: string,twin:boolean} = {email: '', childName: '', school: '',schoolId:-1,  hebSchool: '',hebSchoolId:-1,DOB: null,rankings: [{name:"Main Sanctuary",value: 0},{name:"Family Minyan",value: 0},{name:"Torah In The Round",value: 0}],nonDates:[],accommodation:false,accommodation_other:'',twin:false};


	set_email(email:string){
		this.entry.email=email;
	}


	avoid_days: DoubleDate[];

  constructor() {


  }

}
