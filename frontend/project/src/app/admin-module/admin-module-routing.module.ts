import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AdminModulePageComponent } from './admin-module-page/admin-module-page.component';

const routes: Routes = [
    {
      path: '',
      component: AdminModulePageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class AdminPageRoutingModule { }
  

