import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { FriendsModulePageComponent } from './friends-module-page/friends-module-page.component';

const routes: Routes = [
    {
      path: '',
      component: FriendsModulePageComponent
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
  })
  export class FriendsModuleRoutingModule { }
  

