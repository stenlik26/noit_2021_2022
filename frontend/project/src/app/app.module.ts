import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import {FormsModule} from "@angular/forms";
import {MonacoEditorModule} from "ngx-monaco-editor";
import { MenuComponent } from './menu/menu.component';
import { CreateProblemModule } from './create-problem/create-problem.module';
import { CreateGroupModule } from './create-group/create-group.module';
import '@fortawesome/fontawesome-free/js/all.js';
@NgModule({
  declarations: [
    AppComponent,
    MenuComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    MonacoEditorModule.forRoot(), // use forRoot() in main app module only.
    CreateProblemModule,
    CreateGroupModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
