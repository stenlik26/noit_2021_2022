import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadPicturePageComponent } from './upload-picture-page/upload-picture-page.component';
import { UploadPictureRoutingModule } from './upload-picture-routing.module';


@NgModule({
  declarations: [
    UploadPicturePageComponent
  ],
  imports: [
    CommonModule,
    UploadPictureRoutingModule
  ]
})
export class UploadPictureModule { }
