import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FormVenueComponent } from './form-venue.component';

describe('FormVenueComponent', () => {
  let component: FormVenueComponent;
  let fixture: ComponentFixture<FormVenueComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FormVenueComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FormVenueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
