import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreateGroupPageComponent } from './create-group-page/create-group-page.component';
import { CreateGroupRoutingModule } from './create-group-routing.module';


@NgModule({
  declarations: [
    CreateGroupPageComponent
  ],
  imports: [
    CommonModule,
    CreateGroupModule
  ]
})
export class CreateGroupModule { }
