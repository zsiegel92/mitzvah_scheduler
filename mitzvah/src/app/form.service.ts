import { Injectable } from '@angular/core';
import { DoubleDate } from './DoubleDate';

@Injectable()
export class FormService {
	birthday: DoubleDate;
	avoid_days: DoubleDate[];

  constructor() { }

}
