import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CreateGroupPageComponent } from './create-group-page/create-group-page.component';


const routes: Routes = [
    {
      path: '',
      component: CreateGroupPageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class CreateGroupRoutingModule { }
  

