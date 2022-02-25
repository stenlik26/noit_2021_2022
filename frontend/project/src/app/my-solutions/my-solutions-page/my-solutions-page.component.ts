import { Component, OnInit } from '@angular/core';
import { MySolution } from 'src/app/my-solutions-class';
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';

@Component({
  selector: 'app-my-solutions-page',
  templateUrl: './my-solutions-page.component.html',
  styleUrls: ['./my-solutions-page.component.scss']
})
export class MySolutionsPageComponent implements OnInit {

  my_solutions: Array<MySolution>  = new Array<MySolution>();

  constructor() { }

  ngOnInit(): void {
    if (!UserTokenHandling.isUserTokenSet) {
      UserTokenHandling.setGuestToken();
    }
    this.get_my_solutions();
  }

  get_my_solutions(): void{
    const requestBody = {
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }
    fetch((projectConfig.api_url + 'get_my_solutions'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK')
        {
          json.message.forEach((element: any) => {
            this.my_solutions.push(new MySolution(element));
          });
        }
      });
      console.log(this.my_solutions);
  }

}
