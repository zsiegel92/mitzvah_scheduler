import {Component} from '@angular/core';
import {NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';
// import { Hebcal } from '../app.module';

const now = new Date();

@Component({
 selector: 'app-datepicker',
  styleUrls: ['./datepicker.component.css'],
  templateUrl: './datepicker.component.html',
  providers: [
  	]
})
export class DatepickerComponent {

  model: NgbDateStruct;
  date: {year: number, month: number};

  selectThisWeek() {
    this.model = {year: now.getFullYear(), month: now.getMonth() + 1, day: now.getDate() + 6 - (now.getDay() % 7)};
  }

  // non-Saturdays are disabled
  isDisabled(a_date: NgbDateStruct) {
      const d = new Date(a_date.year, a_date.month - 1, a_date.day);
      return d.getDay() !== 6;
      // return true;
    }

  selectToday() {
    this.model = {year: now.getFullYear(), month: now.getMonth() + 1, day: now.getDate()};
  }



  constructor() {
  	this.selectThisWeek();
  	// this.dp.outsideDays="hidden";
  }
}
