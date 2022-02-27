import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { GradeSolutionPageComponent } from './grade-solution-page/grade-solution-page.component';


const routes: Routes = [
    {
      path: ':solution_id/:group_id',
      component: GradeSolutionPageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class GradeSolutionRoutingModule { }
  

