import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SeeProblemPageComponent } from './see-problem-page/see-problem-page.component';

const routes: Routes = [
    {
      path: ':id',
      component: SeeProblemPageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class SeeProblemRoutingModule { }
  

