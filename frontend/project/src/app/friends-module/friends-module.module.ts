import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FriendsModulePageComponent } from './friends-module-page/friends-module-page.component';
import { FriendsModuleRoutingModule } from './friends-module-routing.module';


@NgModule({
  declarations: [
    FriendsModulePageComponent
  ],
  imports: [
    CommonModule,
    FriendsModuleRoutingModule
  ]
})
export class FriendsModuleModule { }
