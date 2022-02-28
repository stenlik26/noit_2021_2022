import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { MySolutionsPageComponent } from './my-solutions-page/my-solutions-page.component';


const routes: Routes = [
    {
      path: '',
      component: MySolutionsPageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class MySolutionsRoutingModule { }
  

