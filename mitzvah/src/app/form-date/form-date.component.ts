import {Component, Input, OnInit, ViewChild} from '@angular/core';
// import {QueryList, ViewChildren, ViewContainerRef} from '@angular/core';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule,NgForm } from '@angular/forms';

import { DoubleDate } from '../DoubleDate';
import { FormService } from '../form.service';
import { MessageService } from '../message.service';

const now = new Date();

@Component({
  selector: 'app-form-date',
  templateUrl: './form-date.component.html',
  styleUrls: ['./form-date.component.css']
})
export class FormDateComponent implements OnInit {
	@ViewChild("f") f: NgForm;
	// @ViewChildren("dp") dps: QueryList<any>

	birthday: NgbDateStruct = {year: now.getFullYear(), month: now.getMonth() + 1, day: now.getDate()};
	models: DoubleDate[];
	maxDate: NgbDateStruct;
	minDate: NgbDateStruct;
	have_birthday: boolean = false;
	pushed: boolean = false;

	// dps_info(){
	// 	// this.messageService.add('new DP: ' + dd.hgregorian);
	// 	this.messageService.add('dps.length: ' + this.dps.length);
	// 	this.dps.forEach(dp => dp.focus());
	// 	this.dps.forEach(dp=> this.messageService.add(dp.select().year));
	// 	var greg= this.models[this.models.length-1].getGreg();
	// 	this.dps.last.navigateTo({year: greg.year, month: greg.month});
	// }

	push_date() {
		var dd = new DoubleDate();
		if (this.models.length > 0){
			dd.copy_dd(this.models[this.models.length -1]);
		}
		else {
			if (this.birthday.year + 13 <= this.maxDate.year){
				dd.thirteen_from_h(this.birthday);
			}
		}
	  this.models.push(dd);
	  this.pushed=true;
	}

	pop_date(i: number) {
	  this.models.splice(i,1);
	}

	setBirthday(bd: NgbDateStruct){
	  this.have_birthday = true;
	  this.birthday = bd;
	}

	sync(a_dp_component,greg: NgbDateStruct){
	  a_dp_component.navigateTo({ year: greg.year, month: greg.month });
	}

	// sync_all(){
	// 	this.dps.forEach(
	// 	  (dp,index) => {
	// 	  	this.sync(dp,this.models[index].getGreg());
	// 		});
	// }

	isNotSaturday(a_date: NgbDateStruct) {
	    const d = new Date(a_date.year, a_date.month - 1, a_date.day);
	    return d.getDay() !== 6;
	  }

	syncForm(){

	}
	prepForm(){
		this.setBirthday(this.formService.birthday.getGreg());

	}


  constructor(private formService: FormService,private messageService: MessageService) {
  	this.maxDate = {year: now.getFullYear() + 5, month: now.getMonth() + 1, day: now.getDate()};
  	this.minDate = {year: now.getFullYear(), month: now.getMonth() + 1, day: now.getDate()};
  }

  ngOnInit() {
  	this.models=[];
  	this.formService.entry.nonDates=this.models;
  }

}
