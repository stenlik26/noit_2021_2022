import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SolveTaskPageComponent } from './solve-task-page/solve-task-page.component';
import {EditCodeRoutingModule} from "./edit-code-routing.module";
import {MonacoEditorModule} from "ngx-monaco-editor";
import {FormsModule} from "@angular/forms";
import { EditCodeComponent } from './edit-code/edit-code.component';



@NgModule({
  declarations: [
    SolveTaskPageComponent,
    EditCodeComponent
  ],
  imports: [
    CommonModule,
    EditCodeRoutingModule,
    MonacoEditorModule,
    FormsModule
  ]
})
export class EditCodeModule { }
