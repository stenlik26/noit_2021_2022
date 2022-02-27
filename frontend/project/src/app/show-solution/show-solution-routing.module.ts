import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ShowSolutionPageComponent } from './show-solution-page/show-solution-page.component';


const routes: Routes = [
    {
      path: ':code_id',
      component: ShowSolutionPageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class ShowSolutionRoutingModule { }
  

