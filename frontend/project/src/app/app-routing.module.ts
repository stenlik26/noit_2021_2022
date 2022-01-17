import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    loadChildren: () => import('./home/home-routing.module').then(m => m.HomeRoutingModule)
  },
  {
    path: 'solve',
    loadChildren: () => import('./edit-code/edit-code.module').then(m => m.EditCodeModule)
  },
  {
    path: 'register',
    loadChildren: () => import('./register/register-routing.module').then(m => m.RegisterRoutingModule)
  },
  {
    path: 'login',
    loadChildren: () => import('./login/login-routing.module').then(m => m.LoginRoutingModule)
  },
  {
    path: 'create_problem',
    loadChildren: () => import('./create-problem/create-problem-routing.module').then(m => m.CreateProblemRoutingModule)
  },
  {
    path: 'create_group',
    loadChildren: () => import('./create-group/create-group-routing.module').then(m => m.CreateGroupRoutingModule)
  },
  {
    path: 'not_found',
    loadChildren: () => import('./not_found_module/not_found_routing.module').then(m => m.NotFoundRoutingModule)
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
//@ts-ignore
export class AppRoutingModule { }
