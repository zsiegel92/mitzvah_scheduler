import { Component, Inject, OnInit } from '@angular/core';
import { ActivatedRoute, Router, UrlSegment} from '@angular/router';
import 'rxjs/add/operator/finally';
import { DOCUMENT } from '@angular/platform-browser'

import { Location } from '@angular/common';
import { DataService } from '../data.service'

@Component({
  selector: 'app-submissions',
  templateUrl: './submissions.component.html',
  styleUrls: ['./submissions.component.css']
})
export class SubmissionsComponent implements OnInit {
	code: string='blank';
	submissions: any[] = [];
  base_url: string = "";
  full_url: string = "";
  code_accepted: boolean = false;

  constructor(@Inject(DOCUMENT) document: any, private route: ActivatedRoute,private router: Router,private location: Location,private dataService: DataService) {
  	// this.document = document;
  	this.base_url=document.location.origin;
  	this.full_url = document.location.href;
  }


  getSubmissions(){
  	this.dataService.getSubmissions(this.code).subscribe(submissions => {
  		this.submissions = submissions;
  		this.code_accepted = true;
  	});
  }

  blank_route(){
  	const segments: UrlSegment[] = this.route.snapshot.url;
  	if (segments.length > 1) {
  		const url = this
  		        .router
  		        .createUrlTree(['../'], {relativeTo: this.route})
  		        .toString();
  		 this.location.go(url);
  	}
  }

  ngOnInit() {
				this.route
  	            .params
  	            .subscribe(params => {
  	            	this.code=params.code ? params.code : '';
  	            	this.getSubmissions();
  	            	this.blank_route();
  	            });
  }

}
