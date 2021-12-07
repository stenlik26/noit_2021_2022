import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { EditCodePageComponent} from './edit-code-page/edit-code-page.component';


const routes: Routes = [
  {
    path: ':id',
    component: EditCodePageComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EditCodeRoutingModule { }
