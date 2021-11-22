import { Component, OnInit } from '@angular/core';
import { UserTokenHandling } from 'src/app/user_token_handling';
import projectConfig from '../../../assets/conf.json'

@Component({
  selector: 'app-create-group-page',
  templateUrl: './create-group-page.component.html',
  styleUrls: ['./create-group-page.component.scss']
})
export class CreateGroupPageComponent implements OnInit {

  constructor() { }

  async api_output(apiStatus: any): Promise<void> {
    const statusString = document.getElementById('status') as HTMLParagraphElement;


    if(apiStatus.status === 'OK')
    {
      statusString.style.color = 'green';
      statusString.textContent = 'Успешено е създадена групата!';
      window.location.href = projectConfig.site_url;
    }
    else
    {
      statusString.style.color = 'red';
      statusString.textContent = 'Възникна проблем!';
    }
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
          this.api_output(json);
        });
  }

  create_group_button(): void {
    const name: string = (document.getElementById('group_name') as HTMLInputElement).value;
    const statusString = (document.getElementById('status') as HTMLInputElement);

    if (name !== '') {
      this.send_request(name);
    }
    else {
      statusString.style.color = 'red';
      statusString.textContent = 'Моля попълнете всички полета!';
    }

  }

  back(): void{
    window.location.href = projectConfig.site_url;
  }

  ngOnInit(): void {
    if (!UserTokenHandling.isUserTokenSet) {
      UserTokenHandling.setGuestToken();
    }
  }

}
