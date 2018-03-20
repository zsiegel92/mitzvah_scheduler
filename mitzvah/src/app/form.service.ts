import { Injectable, OnInit} from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { DataService } from './data.service'

import { DoubleDate } from './DoubleDate';
import { School } from './school';

@Injectable()
export class FormService implements OnInit {
	public birthday: DoubleDate;
	public entry: {email: string, childName: string, school: string,schoolId:number,  hebSchool: string,hebSchoolId:number,DOB: Date, rankings: any[],atVenue:boolean,over200: boolean,nonDates: DoubleDate[],accommodation: boolean,accommodation_other: string,twin:boolean,DOBdd: DoubleDate,BMdd:DoubleDate} = {email: '', childName: '', school: '',schoolId:-1,  hebSchool: '',hebSchoolId:-1,DOB: null,rankings: [{name:"Main Sanctuary",value: 0},{name:"Family Minyan",value: 0},{name:"Torah In The Round",value: 0}],atVenue:false,over200:false,nonDates:[],accommodation:false,accommodation_other:'',twin:false,DOBdd:new DoubleDate(),BMdd:new DoubleDate()};

	public schools: School[];
	public hebSchools: School[];
	public all_schools: {schools: School[], hebSchools: School[]} = {schools: [],hebSchools: []};

	getSchools(): void {
		this.dataService.getSchools().subscribe(schs => {
			      	this.schools = schs;
			      	this.all_schools.schools = schs;
			      	}
			      );
	}

	getHebSchools(): void {
	  this.dataService.getHebSchools().subscribe(schs => {
	  	      	this.hebSchools = schs;
	  	      	this.all_schools.hebSchools = schs;
	  	      });
	}
	submit(){
		this.entry.DOBdd.copy_ngb_ducktype({'year': this.entry.DOB.getFullYear(),'month':this.entry.DOB.getMonth(),'day':this.entry.DOB.getDate()});
		this.entry.BMdd.copy_dd(this.entry.DOBdd);
		this.entry.BMdd.thirteen_from_now();
		this.dataService.submit(this.entry).subscribe();
	}

	set_email(email:string){
		this.entry.email=email;
	}


	avoid_days: DoubleDate[];

  constructor(private dataService: DataService) {
  	this.getSchools();
  	this.getHebSchools();
  }

  ngOnInit(){}

}
