import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowSolutionPageComponent } from './show-solution-page.component';

describe('ShowSolutionPageComponent', () => {
  let component: ShowSolutionPageComponent;
  let fixture: ComponentFixture<ShowSolutionPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShowSolutionPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ShowSolutionPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
