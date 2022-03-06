import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';
import { UserInfo } from 'src/app/user_info';
import { MySolution } from 'src/app/my-solutions-class';
import { Modal } from 'bootstrap';

@Component({
  selector: 'app-profile-page-comp',
  templateUrl: './profile-page-comp.component.html',
  styleUrls: ['./profile-page-comp.component.scss']
})
export class ProfilePageCompComponent implements OnInit {

  profile_id: string = '';
  profile_info: UserInfo = null!;
  my_profile: boolean = true;
  shared_solutions: Array<MySolution> = new Array<MySolution>();
  has_shared_solutions: boolean = false;
  current_change_string: string = ''; 
  change_modal: any;
  status:string = '';
  user_is_me_and_admin: boolean = false;

  constructor(private activatedRoute: ActivatedRoute) { 
    if (!UserTokenHandling.isUserLoggedIn()) {
      window.location.href = projectConfig.site_url + 'not_found';
    }
    //@ts-ignore
    this.profile_id = this.activatedRoute.snapshot.paramMap.get('id');
    this.my_profile = (this.profile_id === UserTokenHandling.getUserId());
  }

  ngOnInit(): void {
    this.get_profile_info();
    this.get_shared_solutions();
    //@ts-ignore
    this.change_modal = new Modal(document.getElementById('change_modal'));
    if (this.my_profile)
    {
      this.check_for_admin_panel_access();
    }
  }

  check_for_admin_panel_access(): void
  {
    const data = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId()
    };

    fetch(projectConfig.api_url + 'has_access_to_admin_panel', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-type': 'application/json' }
    }).then(response => response.json()).then(json => {
      this.user_is_me_and_admin = json.status === 'OK';
    });
  }

  get_profile_info(): void{
    const requestBody = {
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      profile_id: this.profile_id
    }
    fetch((projectConfig.api_url + 'get_user_info'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if (json.status === 'OK') {
          console.log(json.message);
          this.profile_info = new UserInfo(json.message);
        }
      });
  }

  get_shared_solutions(): void{
    const requestBody = {
      user_id: this.profile_id,
      token: UserTokenHandling.getUserToken()
    }
    fetch((projectConfig.api_url + 'get_shared_solutions'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK')
        {
          json.message.forEach((element: any) => {
            this.shared_solutions.push(new MySolution(element));
          });
          this.has_shared_solutions = (this.shared_solutions.length !== 0);
        }
      });
      console.log(this.shared_solutions);
  }

  show_change_modal(change_num: number): void{
    switch(change_num){
      case 1:
        this.current_change_string = 'име';
        this.change_modal.show();
        break;
      case 2:
        this.current_change_string = 'информация';
        this.change_modal.show();
        break;

    }
  }

  change_info(): void{

    let requestBody = {}

    let url = '';

    this.status = 'Моля изчакайте.';

    let input_field = document.getElementById('change_input') as HTMLInputElement;
    input_field.style.display = 'none';

    switch(this.current_change_string){
      case 'име':
        requestBody = {
          new_name: input_field.value,
          user_id: this.profile_id,
          token: UserTokenHandling.getUserToken()
        }
        url = 'change_user_name';
        break;
      case 'информация':
        requestBody = {
          new_desc: input_field.value,
          user_id: this.profile_id,
          token: UserTokenHandling.getUserToken()
        }
        url = 'change_user_desc';
        break;
    }
    fetch((projectConfig.api_url + url), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK')
        {
          this.get_profile_info();
          this.change_modal.hide();
          input_field.style.display = 'block';
          this.status = '';
          input_field.value = '';
        } 
      });
  }

}
