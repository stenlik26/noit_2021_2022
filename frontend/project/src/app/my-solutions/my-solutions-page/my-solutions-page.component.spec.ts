import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MySolutionsPageComponent } from './my-solutions-page.component';

describe('MySolutionsPageComponent', () => {
  let component: MySolutionsPageComponent;
  let fixture: ComponentFixture<MySolutionsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MySolutionsPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MySolutionsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
