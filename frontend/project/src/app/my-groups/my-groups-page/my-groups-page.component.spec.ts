import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MyGroupsPageComponent } from './my-groups-page.component';

describe('MyGroupsPageComponent', () => {
  let component: MyGroupsPageComponent;
  let fixture: ComponentFixture<MyGroupsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MyGroupsPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MyGroupsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
