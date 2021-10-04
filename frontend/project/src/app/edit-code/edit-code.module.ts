import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EditCodePageComponent } from './edit-code-page/edit-code-page.component';
import {EditCodeRoutingModule} from "./edit-code-routing.module";
import {MonacoEditorModule} from "ngx-monaco-editor";
import {FormsModule} from "@angular/forms";



@NgModule({
  declarations: [
    EditCodePageComponent
  ],
  imports: [
    CommonModule,
    EditCodeRoutingModule,
    MonacoEditorModule,
    FormsModule
  ]
})
export class EditCodeModule { }
