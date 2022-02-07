import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GradeSolutionPageComponent } from './grade-solution-page.component';

describe('GradeSolutionPageComponent', () => {
  let component: GradeSolutionPageComponent;
  let fixture: ComponentFixture<GradeSolutionPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GradeSolutionPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GradeSolutionPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
