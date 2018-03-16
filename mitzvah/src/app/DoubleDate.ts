import * as Hebcal from 'hebcal';
import {NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';

const now = new Date();

export class DoubleDate {
    greg: NgbDateStruct;
    hyear: number;
    hmonth: number;
    hdate: number;
    hday: number;
    hdays_in_month: number;
    hgregorian: Date;
    hgregorian_eve: Date;
    hdate_str: string;
    hdate_str_heb: string;
    holidays: any[];
    // selfdict: {"Gregorian Date": NgbDateStruct,
    // 					"Hebrew Date (Roman)": string,
    // 					"Hebrew Date (Hebrew)": string,
    // 					"Number of days in (Hebrew) month": number,
    // 					"Gregorian Date (backconverted)": string,
    // 					"Gregorian Date Eve (backconverted)": string};

    getGreg(){
    	return this.greg;
    }
    update() {
      var heb = new Hebcal.HDate(new Date(this.greg.year, this.greg.month-1, this.greg.day));
      this.hyear = heb.getFullYear();
      this.hmonth = heb.getMonth();
      this.hdate = heb.getDate();
      this.hday = heb.getDay();
      this.hdays_in_month = heb.daysInMonth();
      this.hgregorian = heb.greg();
      this.hgregorian_eve = heb.gregEve();
      this.hdate_str = heb.toString();
      this.hdate_str_heb= heb.toString('h');
      this.holidays= heb.holidays();  //Try holidays(all)
      // this.to_dict();

    }

    to_dict(){
    	return {"Gregorian Date":this.greg,
    					"Hebrew Date (Roman)":this.hdate_str,
    					"Hebrew Date (Hebrew)":this.hdate_str_heb,
    					"Number of days in (Hebrew) month":this.hdays_in_month,
    					"Gregorian Date (backconverted)":this.hgregorian.toString(),
    					"Gregorian Date Eve (backconverted)": this.hgregorian_eve.toString()}
    }

    thirteen_ago(){
    	this.greg = {year: now.getFullYear()-13,month: now.getMonth()+1,day:now.getDate()}
    	this.update();
    }

    //"If any values are out of range, e.g. the 31st of Nisan, convert them to proper values, i.e. 1st of Iyyar."
    thirteen_from_h(gdate: NgbDateStruct){
    	var heb = new Hebcal.HDate(new Date(gdate.year, gdate.month-1, gdate.day));
    	var future = new Hebcal.HDate(heb.getDate(),heb.getMonth(),heb.getFullYear() + 13).onOrAfter(6).greg();
    	this.greg={year: future.getFullYear(),month: future.getMonth()+1,day:future.getDate()}
    	this.update();
    }

    copy_dd(other: DoubleDate){
    	this.greg={year: other.greg.year,month: other.greg.month,day:other.greg.day}
    	this.update();
    }

    copy_ngb(other: NgbDateStruct){
    	this.greg={year: other.year,month: other.month,day:other.day}
    	this.update();
    }

    selectThisWeek() {
      this.greg = {year: now.getFullYear(), month: now.getMonth()+1, day: now.getDate() + 6 - (now.getDay() % 7)};
      this.update();
    }

    constructor(){
      this.selectThisWeek();
    }
  }
