import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowProblemsPageComponent } from './show-problems-page.component';

describe('ShowProblemsPageComponent', () => {
  let component: ShowProblemsPageComponent;
  let fixture: ComponentFixture<ShowProblemsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShowProblemsPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ShowProblemsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
