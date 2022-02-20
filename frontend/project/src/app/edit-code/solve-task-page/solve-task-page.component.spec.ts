import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SolveTaskPageComponent } from './solve-task-page.component';

describe('EditCodePageComponent', () => {
  let component: SolveTaskPageComponent;
  let fixture: ComponentFixture<SolveTaskPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SolveTaskPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SolveTaskPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
