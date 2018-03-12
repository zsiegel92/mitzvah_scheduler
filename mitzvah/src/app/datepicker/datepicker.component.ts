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
  //TODO: this component gets an input "multi" or "mono", which determines whether it maintains a single ngb-datepicker or several.

  // @Input() multi: boolean;

  // jmodel: NgbDateStruct;


  // jDate: {year: number, month: number,date: number, day: number, days_in_month: number, gregorian: Date, gregorian_eve: Date, date_str: string, date_str_heb: string};

  models: DoubleDate[];

  // maxDate : {year: number, month: number, day: number};

  // minDate: {year: number, month: number, day: number};

  maxDate: NgbDateStruct;
  minDate: NgbDateStruct;

  push_date() {
    this.models.push(new DoubleDate());
  }

  pop_date(i: number) {
    this.models.splice(i,1);
  }

  // selectThisWeek() {
  //   this.model = {year: now.getFullYear(), month: now.getMonth() + 1, day: now.getDate() + 6 - (now.getDay() % 7)};
  //   this.j_update();
  // }

  // j_update() {
  //   var j_selected = new Hebcal.HDate(new Date(this.model.year, this.model.month, this.model.day));
  //   this.jDate = {year: j_selected.getFullYear(), month: j_selected.getMonth(), date: j_selected.getDate(), day: j_selected.getDay(), days_in_month: j_selected.daysInMonth(), gregorian: j_selected.greg(), gregorian_eve: j_selected.gregEve(), date_str: j_selected.toString(),date_str_heb: j_selected.toString('h')};
  // }


  // non-Saturdays are disabled
  isDisabled(a_date: NgbDateStruct) {
      const d = new Date(a_date.year, a_date.month - 1, a_date.day);
      return d.getDay() !== 6;
      // return true;
    }

  constructor() {
    this.models = [new DoubleDate()];
    this.maxDate = {year: now.getFullYear() + 1, month: now.getMonth() + 1, day: now.getDate()};
    this.minDate = {year: now.getFullYear() - 15, month: now.getMonth() + 1, day: now.getDate()};
    // this.push_double_date();
    // this.selectThisWeek();
  }
}
