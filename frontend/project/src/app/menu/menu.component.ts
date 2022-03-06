import { Component, OnInit } from '@angular/core';
import projectConfig from '../../assets/conf.json';
import { UserTokenHandling } from 'src/app/user_token_handling';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent implements OnInit {

  profile_pic: HTMLImageElement = undefined!;
  is_user_logged_in: boolean = false;
  readonly DEFAULT_USER_PICTURE = 'assets/icons/user.png';
  my_user_id: string = '';
  user_name: string = '';

  constructor() { }

  ngOnInit(): void {
    if (UserTokenHandling.isUserLoggedIn())
    {
      this.get_profile_info();
      this.is_user_logged_in = true;
      this.my_user_id = UserTokenHandling.getUserId()!;
    }
  }

  get_profile_info(): void{
    const requestBody = {
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      profile_id: UserTokenHandling.getUserId()
    }
    fetch((projectConfig.api_url + 'get_user_info'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if (json.status === 'OK') {
          this.profile_pic = document.getElementById('user-profile-pic') as HTMLImageElement;

          if(json.message.picture === '')
          {
            this.profile_pic.src = this.DEFAULT_USER_PICTURE;
          }
          else{
            this.profile_pic.src = projectConfig.picture_url + json.message.picture;
          }

          this.user_name = json.message.name;

        }
      });
  }


  logout(): void{
    UserTokenHandling.logOut();
    window.location.href = projectConfig.site_url;
  }
}
