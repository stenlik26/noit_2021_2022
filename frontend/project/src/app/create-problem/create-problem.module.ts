import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreateProblemPageComponent } from './create-problem-page/create-problem-page.component';
import { CreateProblemRoutingModule } from './create-problem-routing.module';


@NgModule({
  declarations: [
    CreateProblemPageComponent
  ],
  imports: [
    CommonModule,
    CreateProblemRoutingModule
  ]
})
export class CreateProblemModule { }
