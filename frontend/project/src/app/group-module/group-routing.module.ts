import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { GroupModulePageComponent } from './group-module-page/group-module-page.component';


const routes: Routes = [
    {
      path: ':id',
      component: GroupModulePageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class GroupRoutingModule { }
  

