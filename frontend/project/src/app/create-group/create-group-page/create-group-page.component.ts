import { Component, OnInit } from '@angular/core';
import { UserTokenHandling } from 'src/app/user_token_handling';
import projectConfig from '../../../assets/conf.json'
import { UserInfo } from 'src/app/user_info';

@Component({
  selector: 'app-create-group-page',
  templateUrl: './create-group-page.component.html',
  styleUrls: ['./create-group-page.component.scss']
})
export class CreateGroupPageComponent implements OnInit {

  constructor() { 
  }

  first_panel: any;
  second_panel: any;
  success_page: any;
  all_users: Array<UserInfo> = new Array<UserInfo>();
  users_to_invite: Array<string> = new Array<string>();

  async create_group_output(apiMessage: any): Promise<void> {
    const statusString = document.getElementById('status') as HTMLParagraphElement;

    if(apiMessage.status === 'OK')
    {
      this.send_group_invites(apiMessage.group_id);
    }
    else
    {
      statusString.style.color = 'red';
      statusString.textContent = 'Възникна проблем!';
    }
  }

  user_info_to_list(apiMessage: any): void{
    apiMessage.message.forEach((element: any) => {
      this.all_users.push(new UserInfo(element))
    });
  }

  send_request(name: string): void {
    const requestBody = {
      group_name: name,
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId()
    };

    fetch((projectConfig.api_url + 'create_group'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
        .then(response => response.json())
        .then(json => {
          this.create_group_output(json);
        });
  }

  send_group_invites(group_id: string): void{
    const requestBody = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId(),
      group_id: group_id,
      invited_ids: this.users_to_invite
    };

    fetch((projectConfig.api_url + 'send_multiple_group_invites'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
        .then(response => response.json())
        .then(json => {
          const statusString = document.getElementById('status') as HTMLParagraphElement;
          if(json.status == 'OK')
          {
            statusString.style.color = 'green';
            statusString.textContent = 'Успешено е създадена групата!';
            this.second_panel.style.display = 'none';
            this.success_page.style.display = 'block';
          }
          else{
            statusString.style.color = 'red';
            statusString.textContent = 'Възникна с изпращането на поканите!';
          }
        });
  }

  create_group_button(): void {
    const name: string = (document.getElementById('group_name') as HTMLInputElement).value;
    const statusString = (document.getElementById('status') as HTMLInputElement);

    statusString.style.color = 'yellow';
    statusString.textContent = 'Моля изчакайте...';

    if (name !== '') {
      this.send_request(name);
    }
    else {
      statusString.style.color = 'red';
      statusString.textContent = 'Моля попълнете всички полета!';
    }

  }

  get_users_to_invite(): void{
    const requestBody = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId()
    };

    fetch((projectConfig.api_url + 'get_all_users'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
        .then(response => response.json())
        .then(json => {
          this.user_info_to_list(json);
        });
  }

  back(): void{
    window.location.href = projectConfig.site_url;
  }

  next_page(): void{
    this.first_panel.style.display = "none";
    this.second_panel.style.display = "block";
  }

  previous_page(): void{
    this.first_panel.style.display = "block";
    this.second_panel.style.display = "none";
  }

  ngOnInit(): void {
    if (!UserTokenHandling.isUserTokenSet) {
      UserTokenHandling.setGuestToken();
    }
    this.first_panel = document.getElementById('main_panel') as HTMLDivElement;
    this.second_panel = document.getElementById('second_panel') as HTMLDivElement;
    this.success_page = document.getElementById('success_page') as HTMLDivElement;
    this.get_users_to_invite();
  }

  add_user_to_invite_list(user_id: string): void{
    this.users_to_invite.push(user_id);
    const inviteButton = document.getElementById(user_id + '_invite') as HTMLButtonElement;
    const removeButton = document.getElementById(user_id + '_remove') as HTMLButtonElement;

    inviteButton.style.display = 'none';
    removeButton.style.display = 'block';
  }

  remove_user_from_invite_list(user_id: string): void{
    this.users_to_invite.forEach((element, index) => {
      if (element == user_id) this.users_to_invite.splice(index, 1);
    });


    const inviteButton = document.getElementById(user_id + '_invite') as HTMLButtonElement;
    const removeButton = document.getElementById(user_id + '_remove') as HTMLButtonElement;

    inviteButton.style.display = 'block';
    removeButton.style.display = 'none';
  }

}
