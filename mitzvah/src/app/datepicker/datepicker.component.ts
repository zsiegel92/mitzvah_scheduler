import {Component} from '@angular/core';
import {NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';
// import { Hebcal } from '../app.module';
import * as Hebcal from 'hebcal';

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
  // jmodel: NgbDateStruct;
  jDate: {year: number, month: number,date: number, day: number, days_in_month: number, gregorian: Date, gregorian_eve: Date, date_str: string, date_str_heb: string};

  selectThisWeek() {
    this.model = {year: now.getFullYear(), month: now.getMonth() + 1, day: now.getDate() + 6 - (now.getDay() % 7)};
    this.j_update();
  }

  // non-Saturdays are disabled
  isDisabled(a_date: NgbDateStruct) {
      const d = new Date(a_date.year, a_date.month - 1, a_date.day);
      return d.getDay() !== 6;
      // return true;
    }

  j_update() {
    var j_selected = new Hebcal.HDate(new Date(this.model.year, this.model.month, this.model.day));
    this.jDate = {year: j_selected.getFullYear(), month: j_selected.getMonth(), date: j_selected.getDate(), day: j_selected.getDay(), days_in_month: j_selected.daysInMonth(), gregorian: j_selected.greg(), gregorian_eve: j_selected.gregEve(), date_str: j_selected.toString(),date_str_heb: j_selected.toString('h')};
  }

  constructor() {
  	this.selectThisWeek();
  	// this.dp.outsideDays="hidden";
  }
}
