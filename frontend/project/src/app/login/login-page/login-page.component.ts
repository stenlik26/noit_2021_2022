import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { sha256 } from 'js-sha256';
import { UserTokenHandling } from 'src/app/user_token_handling';
import projectConfig from '../../../assets/conf.json'

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss']
})
export class LoginPageComponent implements OnInit {

  constructor(private router: Router) { }

  async loginApiOutput(apiStatus: any): Promise<void> {
    const statusString = document.getElementById('status') as HTMLParagraphElement;

    switch (apiStatus.status)
    {
      case 'OK':
      {
        statusString.style.color = 'green';
        statusString.textContent = 'Успешен вход!';
        UserTokenHandling.setUserToken(apiStatus.token);
        UserTokenHandling.setUserToId(apiStatus.userId);
        window.location.href = projectConfig.site_url;
        break;
      }
      case 'error_no_such_user':
      {
        statusString.style.color = 'red';
        statusString.textContent = 'Потребител с такова име не същестува';
        break;
      }
      case 'error_wrong_password':
      {
        statusString.style.color = 'red';
        statusString.textContent = 'Грешна парола.';
        break;
      }
      default:
      {
        statusString.style.color = 'red';
        statusString.textContent = 'Възникна проблем!';
        break;
      }
    }
  }
  sendLoginRequest(name: string, password: string): void {
    const requestBody = {
      email: name,
      password: sha256(password),
    };

    fetch((projectConfig.api_url + 'login_user'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
        .then(response => response.json())
        .then(json => {
          this.loginApiOutput(json);
        });
  }

  loginBtn(): void {
    const name: string = (document.getElementById('email') as HTMLInputElement).value;
    const password: string = (document.getElementById('password') as HTMLInputElement).value;
    const statusString = (document.getElementById('status') as HTMLInputElement);

    if (name === '' || password === '') {
      statusString.style.color = 'red';
      statusString.textContent = 'Моля попълнете всички полета!';
    }
    else {
      this.sendLoginRequest(name, password);
    }
  }
  ngOnInit(): void {
    if (!UserTokenHandling.isUserTokenSet) {
      UserTokenHandling.setGuestToken();
    }
  }

}
