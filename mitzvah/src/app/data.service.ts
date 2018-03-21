import { Injectable } from '@angular/core';

import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

import { MessageService } from './message.service';
import { School } from './school';
// import { SCHOOLS } from './mock-data';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable()
export class DataService {

	private schoolsURL = 'api/schools';  // URL to web api
	private hebSchoolsURL = 'api/hebschools';  // URL to web api
	private submissionsURL = 'api/submission';
	private getSubmissionsURL = 'api/submissions';

	/** GET schools from the server */
	getSchools (): Observable<School[]> {
		// this.messageService.add('DataService: fetched schools');
	  return this.http.get<School[]>(this.schoolsURL)
	  	.pipe(
	  	      tap(schools => this.log(`fetched schools`)),
	  	      catchError(this.handleError('getSchools',[]))
	  	      );
	}

	/** GET schools from the server */
	getHebSchools (): Observable<School[]> {
		// this.messageService.add('DataService: fetched hebrew schools');
	  return this.http.get<School[]>(this.hebSchoolsURL)
	  	.pipe(
	  	      tap(schools => this.log(`fetched hebrew schools`)),
	  	      catchError(this.handleError('getHebSchools',[]))
	  	      );
	}

	/** GET school by id. Will 404 if id not found */
	getSchool(id: number): Observable<School> {
	  const url = `${this.schoolsURL}/id/${id}`;
	  return this.http.get<School>(url).pipe(
	    tap(_ => this.log(`fetched school id=${id}`)),
	    catchError(this.handleError<School>(`getSchool id=${id}`))
	  );
	}

	/** GET school by id. Will 404 if id not found */
	getHebSchool(id: number): Observable<School> {
	  const url = `${this.hebSchoolsURL}/id/${id}`;
	  return this.http.get<School>(url).pipe(
	    tap(_ => this.log(`fetched hebrew school id=${id}`)),
	    catchError(this.handleError<School>(`getHebSchool id=${id}`))
	  );
	}


	/** POST: add a new school to the server */
	addSchool (school: School): Observable<School> {
	  return this.http.post<School>(`${this.schoolsURL}/add`, school, httpOptions).pipe(
	    tap((school: School) => this.log(`added school w/ id=${school.id}`)),
	    catchError(this.handleError<School>('addSchool'))
	  );
	}

	submit(entry: any): Observable<any>{
		// console.log(entry);
		return this.http.post<any>(this.submissionsURL, entry, httpOptions).pipe(
			    tap((entry: any) => this.log('submitted entry')),
			    catchError(this.handleError<any>('submit'))
			  );
	}

	getSubmissions(code: any): Observable<any> {
		return this.http.post<any>(this.getSubmissionsURL,{'code':code},httpOptions);
	}

	/**
	 * Handle Http operation that failed.
	 * Let the app continue.
	 * @param operation - name of the operation that failed
	 * @param result - optional value to return as the observable result
	 */
	private handleError<T> (operation = 'operation', result?: T) {
	  return (error: any): Observable<T> => {

	    // TODO: send the error to remote logging infrastructure
	    console.error(error); // log to console instead

	    // TODO: better job of transforming error for user consumption
	    this.log(`${operation} failed: ${error.message}`);

	    // Let the app keep running by returning an empty result.
	    return of(result as T);
	  };
	}
	private log(message: string) {
	  this.messageService.add('DataService: ' + message);
	}

  constructor(private http: HttpClient,private messageService: MessageService) { }

}
