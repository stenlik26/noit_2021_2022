import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SeeProblemPageComponent } from './see-problem-page/see-problem-page.component';
import { SeeProblemRoutingModule } from './see-problem-routing.module';


@NgModule({
  declarations: [
    SeeProblemPageComponent
  ],
  imports: [
    CommonModule,
    SeeProblemRoutingModule
  ]
})
export class SeeProblemModule { }
