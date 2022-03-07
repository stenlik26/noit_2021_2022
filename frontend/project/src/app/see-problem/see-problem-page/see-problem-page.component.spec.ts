import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeeProblemPageComponent } from './see-problem-page.component';

describe('SeeProblemPageComponent', () => {
  let component: SeeProblemPageComponent;
  let fixture: ComponentFixture<SeeProblemPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeeProblemPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SeeProblemPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
