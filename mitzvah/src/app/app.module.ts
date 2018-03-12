import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms'; // <-- NgModel lives here
import { HttpClientModule }    from '@angular/common/http';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
// import { Hebcal } from '../../node_modules/hebcal/client/hebcal.min';
// exports: [ Hebcal ],
// Hebcal, (in imports)
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { FormComponent } from './form/form.component';
import { DataService } from './data.service';
import { MessagesComponent } from './messages/messages.component';
import { MessageService } from './message.service';
import { NotFoundComponent } from './not-found/not-found.component';
import { SchoolSelectorComponent } from './school-selector/school-selector.component';
import { DatepickerComponent } from './datepicker/datepicker.component';
import { FormService } from './form.service';
import { FormStudentComponent } from './form-student/form-student.component';
import { FormVenueComponent } from './form-venue/form-venue.component';
import { FormDateComponent } from './form-date/form-date.component';
import { FormAccommodationComponent } from './form-accommodation/form-accommodation.component';

// import * as Hebcal from 'hebcal';

@NgModule({
  declarations: [
    AppComponent,
    FormComponent,
    MessagesComponent,
    NotFoundComponent,
    SchoolSelectorComponent,
    DatepickerComponent,
    FormStudentComponent,
    FormVenueComponent,
    FormDateComponent,
    FormAccommodationComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    NgbModule.forRoot(),
  ],
  providers: [ DataService, MessageService, FormService,],
  bootstrap: [AppComponent]
})
export class AppModule { }
