import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GroupModulePageComponent } from './group-module-page.component';

describe('GroupModulePageComponent', () => {
  let component: GroupModulePageComponent;
  let fixture: ComponentFixture<GroupModulePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GroupModulePageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GroupModulePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
