import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FormAccommodationComponent } from './form-accommodation.component';

describe('FormAccommodationComponent', () => {
  let component: FormAccommodationComponent;
  let fixture: ComponentFixture<FormAccommodationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FormAccommodationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FormAccommodationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
