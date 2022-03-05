import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfilePageCompComponent } from './profile-page-comp.component';

describe('ProfilePageCompComponent', () => {
  let component: ProfilePageCompComponent;
  let fixture: ComponentFixture<ProfilePageCompComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfilePageCompComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfilePageCompComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
