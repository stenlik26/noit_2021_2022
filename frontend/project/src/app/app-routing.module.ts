import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'edit',
    loadChildren: () => import('./edit-code/edit-code.module').then(m => m.EditCodeModule)
  },
  {
    path: 'register',
    loadChildren: () => import('./register/register-routing.module').then(m => m.RegisterRoutingModule)
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
