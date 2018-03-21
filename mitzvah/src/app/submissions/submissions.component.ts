import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { DataService } from '../data.service'

@Component({
  selector: 'app-submissions',
  templateUrl: './submissions.component.html',
  styleUrls: ['./submissions.component.css']
})
export class SubmissionsComponent implements OnInit {
	code: string;
	submissions: any[];

  constructor(private route: ActivatedRoute,private dataService: DataService) { }

  ngOnInit() {
				this.route
  	            .params
  	            .subscribe(params => {
  	            	this.code=params.code;
  	            });

  	     this.dataService.getSubmissions(this.code).subscribe(submissions => this.submissions = submissions);
  }

}
