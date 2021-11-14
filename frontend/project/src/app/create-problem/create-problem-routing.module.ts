import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CreateProblemPageComponent } from './create-problem-page/create-problem-page.component';


const routes: Routes = [
    {
      path: '',
      component: CreateProblemPageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class CreateProblemRoutingModule { }
  

