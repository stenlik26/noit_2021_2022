import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { MyGroupsPageComponent } from './my-groups-page/my-groups-page.component';


const routes: Routes = [
    {
      path: '',
      component: MyGroupsPageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class MyGroupsRoutingModule { }
  

