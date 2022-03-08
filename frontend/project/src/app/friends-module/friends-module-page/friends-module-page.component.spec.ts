import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FriendsModulePageComponent } from './friends-module-page.component';

describe('FriendsModulePageComponent', () => {
  let component: FriendsModulePageComponent;
  let fixture: ComponentFixture<FriendsModulePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FriendsModulePageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FriendsModulePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
