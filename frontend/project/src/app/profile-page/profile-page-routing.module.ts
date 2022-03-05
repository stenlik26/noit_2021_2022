import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ProfilePageCompComponent } from './profile-page-comp/profile-page-comp.component';

const routes: Routes = [
    {
      path: ':id',
      component: ProfilePageCompComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class ProfilePageRoutingModule { }
  

