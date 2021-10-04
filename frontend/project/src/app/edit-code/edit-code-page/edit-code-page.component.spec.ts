import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditCodePageComponent } from './edit-code-page.component';

describe('EditCodePageComponent', () => {
  let component: EditCodePageComponent;
  let fixture: ComponentFixture<EditCodePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EditCodePageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EditCodePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
