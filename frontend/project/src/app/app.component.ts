import { Component } from '@angular/core';
import { UserTokenHandling } from './user_token_handling';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'project';

  constructor(){
    UserTokenHandling.getUserToken();
  }
}
