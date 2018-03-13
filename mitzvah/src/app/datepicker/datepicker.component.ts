import {Component, Input, OnInit, ViewChild} from '@angular/core';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { DoubleDate } from '../DoubleDate';
// import { Hebcal } from '../app.module';
// import * as Hebcal from 'hebcal';

const now = new Date();


@Component({
 selector: 'app-datepicker',
  styleUrls: ['./datepicker.component.css'],
  templateUrl: './datepicker.component.html',
  providers: [
  	]
})
export class DatepickerComponent {
  // @ViewChild('dp') dp: ngbDatepicker;

  @Input()
  onlySaturdays: boolean = true;
  @Input()
  multi: boolean = true;

  // @Input()
  birthday: NgbDateStruct = {year: now.getFullYear(), month: now.getMonth() + 1, day: now.getDate()};

  models: DoubleDate[];

  maxDate: NgbDateStruct;
  minDate: NgbDateStruct;
  have_birthday: boolean = false;

  getModels(){
    return this.models;
  }

  push_date() {
    this.models.push(new DoubleDate());
  }

  pop_date(i: number) {
    this.models.splice(i,1);
  }

  setBirthday(bd: NgbDateStruct){
    this.have_birthday = true;
    this.birthday = bd;
  }

  constructor() {
    this.maxDate = {year: now.getFullYear() + 1, month: now.getMonth() + 1, day: now.getDate()};
    this.minDate = {year: now.getFullYear() - 15, month: now.getMonth() + 1, day: now.getDate()};
  }
  ngOnInit(){
    if (this.multi) {
      this.models=[];
    }
    else {
      this.models = [new DoubleDate()];
    }
  }

  sync(a_dp_component,greg: NgbDateStruct){
    a_dp_component.navigateTo({ year: greg.year, month: greg.month });
  }
  // non-Saturdays are disabled
  isNotSaturday(a_date: NgbDateStruct) {
      const d = new Date(a_date.year, a_date.month - 1, a_date.day);
      return d.getDay() !== 6;
    }
  allFalse(){
    return false;
  }

}
