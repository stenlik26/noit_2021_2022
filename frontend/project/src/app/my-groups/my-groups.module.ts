import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MyGroupsPageComponent } from './my-groups-page/my-groups-page.component';
import { MyGroupsRoutingModule } from './my-groups-routing.module';


@NgModule({
  declarations: [
    MyGroupsPageComponent
  ],
  imports: [
    CommonModule,
    MyGroupsRoutingModule
  ]
})
export class MyGroupsModule { }
