import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    loadChildren: () => import('./home/home-routing.module').then(m => m.HomeRoutingModule)
  },
  {
    path: 'code',
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
  },
  {
    path: 'show_problems',
    loadChildren: () => import('./show-problems/show-problems-routing.module').then(m => m.ShowProblemsRoutingModule)
  },
  {
    path: 'group',
    loadChildren: () => import('./group-module/group-routing.module').then(m => m.GroupRoutingModule)
  },
  {
    path: 'grade_solution',
    loadChildren: () => import('./grade-solution/grade-solution.module').then(m => m.GradeSolutionModule)
  },
  {
    path: 'my_groups',
    loadChildren: () => import('./my-groups/my-groups.module').then(m => m.MyGroupsModule)
  },
  {
    path: 'my_solutions',
    loadChildren: () => import('./my-solutions/my-solutions.module').then(m => m.MySolutionsModule)
  },
  {
    path: 'show_solution',
    loadChildren: () => import('./show-solution/show-solution.module').then(m => m.ShowSolutionModule)
  },
  {
    path: 'profile',
    loadChildren: () => import('./profile-page/profile-page.module').then(m => m.ProfilePageModule)
  },
  {
    path: 'upload_picture',
    loadChildren: () => import('./upload-picture/upload-picture.module').then(m => m.UploadPictureModule)
  },
  {
    path: 'admin_page',
    loadChildren: () => import('./admin-module/admin-module.module').then(m => m.AdminModuleModule)
  },
  {
    path: 'my_friends',
    loadChildren: () => import('./friends-module/friends-module.module').then(m => m.FriendsModuleModule)
  },
  {
    path: 'see_problem',
    loadChildren: () => import('./see-problem/see-problem.module').then(m => m.SeeProblemModule)
  },
  {
    path: '**',
    redirectTo: '/not_found'
  }
  // Note: Ако се добавят нови страници, те трябва да са над това със path: **. В противен случай не работят.
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
//@ts-ignore
export class AppRoutingModule { }
