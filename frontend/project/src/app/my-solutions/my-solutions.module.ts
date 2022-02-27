import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MySolutionsPageComponent } from './my-solutions-page/my-solutions-page.component';
import { MySolutionsRoutingModule } from './my-solutions-routing.module';


@NgModule({
  declarations: [
    MySolutionsPageComponent
  ],
  imports: [
    CommonModule,
    MySolutionsRoutingModule
  ]
})
export class MySolutionsModule { }
