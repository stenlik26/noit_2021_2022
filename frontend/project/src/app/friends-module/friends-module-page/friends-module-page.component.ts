import { Component, OnInit } from '@angular/core';
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';
import { Modal } from 'bootstrap';
import { UserInfo } from 'src/app/user_info';

@Component({
  selector: 'app-friends-module-page',
  templateUrl: './friends-module-page.component.html',
  styleUrls: ['./friends-module-page.component.scss']
})
export class FriendsModulePageComponent implements OnInit {

  constructor() { }

  has_invites: boolean = false;
  my_invites: Array<any> = new Array<any>();
  invites_modal: Modal = undefined!;
  search_modal: Modal = undefined!;
  all_users: Array<UserInfo> = new Array<UserInfo>();
  my_friends: Array<UserInfo> = new Array<UserInfo>();

  ngOnInit(): void {
    if (!UserTokenHandling.isUserLoggedIn()) {
      window.location.href = projectConfig.site_url + 'not_found';
    }
    this.get_my_invites();
    this.get_users_to_invite("?");
    //@ts-ignore
    this.invites_modal = new Modal(document.getElementById('invites_modal'));
    //@ts-ignore
    this.search_modal = new Modal(document.getElementById('search_modal'));
    this.get_my_friends();
  }

  get_my_invites(): void{
    const requestBody = {
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }
    fetch((projectConfig.api_url + 'get_friend_requests'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK')
        {
          this.my_invites = json.message;
          this.has_invites = (json.message.length != 0);
          console.log(this.my_invites);
        }
      });
  }

  show_my_invites(): void{
    this.invites_modal.show();
  }

  show_search_modal(): void{
    this.search_modal.show();
  }

  search_users_by_name(){
    const name = (document.getElementById('name_search_input') as HTMLInputElement).value;
    if(name == "")
    {
      this.get_users_to_invite("?");
    }
    else{
      this.get_users_to_invite(name);
    }
  }

  get_users_to_invite(searched_name: string): void {

    this.all_users = [];

    const requestBody = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId(),
      searched_name: searched_name
    };

    fetch((projectConfig.api_url + 'search_for_user'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        json.message.forEach((element: any) => {
          this.all_users.push(new UserInfo(element))
        });
      });
  }

  open_user_page(user_id: string): void{
    window.open(projectConfig.site_url + "/profile/" + user_id);
  }

  approve_friend_request(request_id: string)
  {
    const requestBody = {
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      request_id: request_id
    }
    fetch((projectConfig.api_url + 'approve_friend_request'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK')
        {
          this.get_my_invites();
          this.get_my_friends();
        }
      }); 
  }

  decline_friend_request(request_id: string){
    const requestBody = {
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      request_id: request_id
    }
    fetch((projectConfig.api_url + 'remove_friend_request'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK')
        {
          this.get_my_invites();
        }
      }); 
  }

  get_my_friends(): void{
    
    this.my_friends = [];

    const requestBody = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId()
    };

    fetch((projectConfig.api_url + 'get_friends_list'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        json.message.forEach((element: any) => {
          this.my_friends.push(new UserInfo(element))
        });
      });
  }

  remove_friend(friend_id: string): void{
    
    const requestBody = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId(),
      friend_id: friend_id
    };

    fetch((projectConfig.api_url + 'remove_friend'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK')
        {
          this.get_my_friends();
        }
      });
  }
}
