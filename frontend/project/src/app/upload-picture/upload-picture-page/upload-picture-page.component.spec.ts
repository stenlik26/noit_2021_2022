import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadPicturePageComponent } from './upload-picture-page.component';

describe('UploadPicturePageComponent', () => {
  let component: UploadPicturePageComponent;
  let fixture: ComponentFixture<UploadPicturePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UploadPicturePageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UploadPicturePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
