import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ShowSolutionPageComponent } from './show-solution-page/show-solution-page.component';
import { ShowSolutionRoutingModule } from './show-solution-routing.module';
import {MonacoEditorModule} from "ngx-monaco-editor";
import {FormsModule} from "@angular/forms";

@NgModule({
  declarations: [
    ShowSolutionPageComponent
  ],
  imports: [
    CommonModule,
    ShowSolutionRoutingModule,
    MonacoEditorModule,
    FormsModule
  ]
})
export class ShowSolutionModule { }
