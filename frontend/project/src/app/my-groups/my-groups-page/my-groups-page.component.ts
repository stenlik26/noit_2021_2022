import { Component, OnInit } from '@angular/core';
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';
import { Modal } from 'bootstrap';

@Component({
  selector: 'app-my-groups-page',
  templateUrl: './my-groups-page.component.html',
  styleUrls: ['./my-groups-page.component.scss']
})
export class MyGroupsPageComponent implements OnInit {

  constructor() { }
  my_groups: any;
  has_invites: boolean = false;
  my_invites: any;
  invites_modal: any;


  ngOnInit(): void {
    if (!UserTokenHandling.isUserTokenSet) {
      UserTokenHandling.setGuestToken();
    }
    this.get_my_groups();
    this.get_my_invites();
    //@ts-ignore
    this.invites_modal = new Modal(document.getElementById('invites_modal'));
  }

  open_invites_modal(): void
  {
    this.invites_modal.show();
  }

  get_my_groups(): void{
    const requestBody = {
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }
    fetch((projectConfig.api_url + 'get_my_groups'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK')
        {
          this.my_groups = json.message;
        }
      });
  }

  get_my_invites(): void{
    const requestBody = {
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }
    fetch((projectConfig.api_url + 'get_user_group_invites'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK')
        {
          this.my_invites = json.message;
          console.log(json.message);
          if(json.message.length != 0)
          {
            this.has_invites = true;
          }
          else{
            this.has_invites = false;
          }
        }
      });
  }

  accept_invite(group_id: string): void{
    const requestBody = {
      my_user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      group_id: group_id
    }
    fetch((projectConfig.api_url + 'accept_group_invite'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK')
        {
          this.get_my_invites();
          this.get_my_groups();
        }
      });
  }

  decline_invite(group_id: string): void{
    const requestBody = {
      my_user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      group_id: group_id
    }
    fetch((projectConfig.api_url + 'reject_group_invite'), {
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

}
