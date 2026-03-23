import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApplicantDashboard } from './applicant-dashboard';

describe('ApplicantDashboard', () => {
  let component: ApplicantDashboard;
  let fixture: ComponentFixture<ApplicantDashboard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ApplicantDashboard],
    }).compileComponents();

    fixture = TestBed.createComponent(ApplicantDashboard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
