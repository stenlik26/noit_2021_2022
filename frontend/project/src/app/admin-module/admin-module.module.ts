import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminModulePageComponent } from './admin-module-page/admin-module-page.component';
import { AdminPageRoutingModule} from './admin-module-routing.module';


@NgModule({
  declarations: [
    AdminModulePageComponent
  ],
  imports: [
    CommonModule,
    AdminPageRoutingModule
  ]
})
export class AdminModuleModule { }
