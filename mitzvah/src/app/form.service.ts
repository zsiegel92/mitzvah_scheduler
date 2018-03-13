import { Injectable } from '@angular/core';
import { DoubleDate } from './DoubleDate';

@Injectable()
export class FormService {
	public birthday: DoubleDate;
	avoid_days: DoubleDate[];

  constructor() { }

}
