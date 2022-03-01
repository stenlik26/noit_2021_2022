import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { UploadPicturePageComponent } from './upload-picture-page/upload-picture-page.component';

const routes: Routes = [
    {
      path: '',
      component: UploadPicturePageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class UploadPictureRoutingModule { }
  

