import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ShowProblemsPageComponent } from './show-problems-page/show-problems-page.component';


const routes: Routes = [
    {
      path: '',
      component: ShowProblemsPageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class ShowProblemsRoutingModule { }
  

