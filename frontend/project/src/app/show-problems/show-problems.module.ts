import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ShowProblemsPageComponent } from './show-problems-page/show-problems-page.component';
import { ShowProblemsRoutingModule } from './show-problems-routing.module';


@NgModule({
  declarations: [
    ShowProblemsPageComponent
  ],
  imports: [
    CommonModule,
    ShowProblemsRoutingModule
  ]
})
export class ShowProblemsModule { }
