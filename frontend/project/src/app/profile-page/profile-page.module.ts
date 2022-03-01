import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProfilePageCompComponent } from './profile-page-comp/profile-page-comp.component';
import { ProfilePageRoutingModule } from './profile-page-routing.module';


@NgModule({
  declarations: [
    ProfilePageCompComponent
  ],
  imports: [
    CommonModule,
    ProfilePageRoutingModule
  ]
})
export class ProfilePageModule { }
