import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SolveTaskPageComponent} from './solve-task-page/solve-task-page.component';
import {EditCodeComponent} from "./edit-code/edit-code.component";


const routes: Routes = [
  {
    path: '',
    component: EditCodeComponent
  },
  {
    path: 'solve/:id',
    component: SolveTaskPageComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EditCodeRoutingModule { }
