import { TestBed } from '@angular/core/testing';

import { Applicant } from './applicant';

describe('Applicant', () => {
  let service: Applicant;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Applicant);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
