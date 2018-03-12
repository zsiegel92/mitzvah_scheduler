import {Component, Input} from '@angular/core';
import {NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';
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
  @Input()
  onlySaturdays: boolean = true;
  @Input()
  multi: boolean = true;


  models: DoubleDate[];

  maxDate: NgbDateStruct;
  minDate: NgbDateStruct;

  push_date() {
    this.models.push(new DoubleDate());
  }

  pop_date(i: number) {
    this.models.splice(i,1);
  }

  constructor() {
    this.models = [new DoubleDate()];
    this.maxDate = {year: now.getFullYear() + 1, month: now.getMonth() + 1, day: now.getDate()};
    this.minDate = {year: now.getFullYear() - 15, month: now.getMonth() + 1, day: now.getDate()};
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
