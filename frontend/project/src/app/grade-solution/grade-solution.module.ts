import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GradeSolutionPageComponent } from './grade-solution-page/grade-solution-page.component';
import { GradeSolutionRoutingModule } from './grade-solution-routing.module';
import {MonacoEditorModule} from "ngx-monaco-editor";
import {FormsModule} from "@angular/forms";

@NgModule({
  declarations: [
    GradeSolutionPageComponent
  ],
  imports: [
    CommonModule,
    GradeSolutionRoutingModule,
    MonacoEditorModule,
    FormsModule
  ]
})
export class GradeSolutionModule { }
