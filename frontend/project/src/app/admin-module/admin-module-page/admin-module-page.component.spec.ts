import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminModulePageComponent } from './admin-module-page.component';

describe('AdminModulePageComponent', () => {
  let component: AdminModulePageComponent;
  let fixture: ComponentFixture<AdminModulePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AdminModulePageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminModulePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
