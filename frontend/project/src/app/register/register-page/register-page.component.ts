import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { sha256 } from 'js-sha256';
import { UserTokenHandling } from 'src/app/user_token_handling';
import projectConfig from '../../../assets/conf.json'

@Component({
  selector: 'app-register-page',
  templateUrl: './register-page.component.html',
  styleUrls: ['./register-page.component.scss']
})
export class RegisterPageComponent implements OnInit {

  constructor(private router: Router) { }

  validateEmail(email: string): boolean {
    const re = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    return re.test(email);
  }


  async registerApiOutput(apiStatus: any): Promise<void> {

    const statusString = document.getElementById('status') as HTMLParagraphElement;

    switch (apiStatus.status) {
      case 'OK':
        {
          statusString.textContent = 'Успешна регистрация!';
          statusString.style.color = 'green';

          statusString.style.visibility = 'hidden';

          this.router.navigate(['/']);
          break;
        }
      case 'error_name_exists':
        {
          statusString.textContent = 'Потребител с това име вече съществува!';
          statusString.style.color = 'red';
          break;
        }
      case 'error_missing_params':
        {
          console.log(apiStatus);
          break;
        }
      case 'error_fields_not_filled':
        {
          statusString.style.color = 'red';
          statusString.textContent = 'Моля попълнете всички полета!';
          break;
        }
      case 'error_email_exists':
        {
          statusString.style.color = 'red';
          statusString.textContent = 'Този email адрес вече е регистриран!';
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


  sendRegisterRequest(userEmail: string, userName: string, password: string): void {
    const requestBody = {
      name: userName,
      email: userEmail,
      password: sha256(password),
      token: UserTokenHandling.getUserToken()
    };

    fetch((projectConfig.api_url + 'register_user'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        this.registerApiOutput(json);
      });
  }

  registerBtn(): void {
    const email: string = (document.getElementById('email') as HTMLInputElement).value;
    const name: string = (document.getElementById('name') as HTMLInputElement).value;
    const password: string = (document.getElementById('password') as HTMLInputElement).value;
    const passwordRepeat: string = (document.getElementById('password-repeat') as HTMLInputElement).value;
    const statusString = (document.getElementById('status') as HTMLInputElement);

    statusString.style.color = 'yellow';
    statusString.textContent = 'Моля изчакайте...';

    if (email === '' || name === '' || password === '' || passwordRepeat === '') {
      statusString.style.color = 'red';
      statusString.textContent = 'Моля попълнете всички полета!';
      return;
    }

    if (!this.validateEmail(email)) {
      statusString.style.color = 'red';
      statusString.textContent = 'Невалиден email адрес!';
      return;
    }

    if (password != passwordRepeat) {
      statusString.style.color = 'red';
      statusString.textContent = 'Паролите в полетата не съвпадат!';
      return;
    }

    this.sendRegisterRequest(email, name, password);

  }

  ngOnInit(): void {

    if (!UserTokenHandling.isUserTokenSet()) {
      UserTokenHandling.setGuestToken();
    }

  }
}
