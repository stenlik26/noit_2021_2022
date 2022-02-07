import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GroupModulePageComponent } from './group-module-page/group-module-page.component';
import { GroupRoutingModule } from './group-routing.module';


@NgModule({
  declarations: [
    GroupModulePageComponent
  ],
  imports: [
    CommonModule,
    GroupRoutingModule
  ]
})
export class GroupModuleModule { }
