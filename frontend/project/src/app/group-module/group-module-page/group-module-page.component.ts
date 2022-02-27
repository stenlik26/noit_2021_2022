import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';
import { ProblemInformationPick } from 'src/app/problem_info_pick';
import { UserInfo } from 'src/app/user_info';
import { SolutionInfo } from 'src/app/solution_info';
import { Modal } from 'bootstrap';


@Component({
  selector: 'app-group-module-page',
  templateUrl: './group-module-page.component.html',
  styleUrls: ['./group-module-page.component.scss']
})
export class GroupModulePageComponent implements OnInit {

  group_id: any;
  is_admin: boolean = false;
  group_title: string = '';
  users: Array<UserInfo> = new Array<UserInfo>();
  users_by_ids: Map<string, UserInfo> = new Map<string, UserInfo>();
  problems: Array<ProblemInformationPick> = new Array<ProblemInformationPick>();
  solutions: Array<SolutionInfo> = new Array<SolutionInfo>();
  all_users: Array<UserInfo> = new Array<UserInfo>();
  invite_modal: any;
  users_to_invite: Array<string> = new Array<string>();
  success_modal: any;
  success_message: any;
  ask_again_modal: any;
  ask_again_message: any;
  current_selected_user: string = '';
  current_clicked_option: string = '';
  change_group_name_modal: any;
  selected_task: string = '';
  time_limit_modal: any;

  ngOnInit(): void {

    this.switchTab('group_members');
    this.get_group_info();
    this.get_user_solutions();
    //@ts-ignore
    this.invite_modal = new Modal(document.getElementById('invite_modal'));
    this.get_users_to_invite();
    //@ts-ignore
    this.success_modal = new Modal(document.getElementById('success_modal'));
    this.success_message = document.getElementById('success_message') as HTMLParagraphElement;
    //@ts-ignore
    this.ask_again_modal = new Modal(document.getElementById('ask_again_modal'));
    this.ask_again_message = document.getElementById('ask_again_message') as HTMLParagraphElement;
    //@ts-ignore
    this.change_group_name_modal = new Modal(document.getElementById('change_group_name_modal'));
    //@ts-ignore
    this.time_limit_modal = new Modal(document.getElementById('time_limit_modal'));
  }

  constructor(private activatedRoute: ActivatedRoute) {
    this.group_id = this.activatedRoute.snapshot.paramMap.get('id');
    this.check_for_access();
  }

  check_for_access(): void {
    const requestBody = {
      group_id: this.group_id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }
    fetch((projectConfig.api_url + 'get_group_access_level'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        switch (json.status) {
          case 'error_no_access': {
            window.location.href = projectConfig.site_url + 'not_found';
            break;
          }
          case 'OK': {
            this.is_admin = (json.message === "admin");
            break;
          }
          default: {
            window.location.href = projectConfig.site_url + 'not_found';
            break;    
          }
        }
      });
  }

  change_group_name_popup(): void{
    this.change_group_name_modal.show();
  }

  solve_problem(time_limit: string, object_id: string){
    if(time_limit === "-1")
    {
      window.location.href = projectConfig.site_url + '/solve/' + object_id;
    }
    else{
      this.time_limit_modal.show();
      this.selected_task = object_id;
    }
  }

  solve_problem_time_limit(object_id: string)
  {
    this.time_limit_modal.hide();
    window.location.href = projectConfig.site_url + '/solve/' + object_id;
  }

  change_group_name(): void{

    const new_group_name = (document.getElementById('new_group_name') as HTMLInputElement).value;

    const requestBody = {
      group_id: this.group_id,
      my_user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      new_name: new_group_name
    }
    fetch((projectConfig.api_url + 'change_group_name'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK'){
          this.success_modal_show(this.change_group_name_modal, "Успешно е сменено името на групата.");
          this.cleanup_after_operation();
        }
      });
  }

  get_group_info(): void{
    const requestBody = {
      group_id: this.group_id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }
    fetch((projectConfig.api_url + 'get_group_data'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK'){
          this.assign_group_info(json.message);
        }
      });
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

  user_info_to_list(apiMessage: any): void{
    apiMessage.message.forEach((element: any) => {
      this.all_users.push(new UserInfo(element))
    });
  }

  async assign_group_info(data: any){
    this.group_title = data.name;
    let num = 1;

    this.problems = [];
    this.users = [];
    this.users_by_ids.clear();

    data.problems.forEach((element: any) => {
      this.problems.push(new ProblemInformationPick(
        num,
        element.title,
        '-',
        [], 
        element._id.$oid, 
        element.start_date, 
        element.end_date, 
        element.is_active,
        element.time_limit))
        num++;
    });

    data.users.forEach((element: any) => {
      this.users.push(new UserInfo(element));
      this.users_by_ids.set(element._id, new UserInfo(element));
    });
    this.get_user_solutions();
  }

  get_user_solutions(){

    this.solutions = [];

    const problem_id = (document.getElementById('problem_selector_box') as HTMLSelectElement).value;
    const user_id = (document.getElementById('user_selector_box') as HTMLSelectElement).value;

    let problem_ids: Array<string> = new Array<string>();

    this.problems.forEach((element: any) => {
      problem_ids.push(element.object_id);
    });

    const requestBody = {
      problem_id: problem_id,
      my_user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      user_id: user_id,
      group_problem_ids: problem_ids
    }
    fetch((projectConfig.api_url + 'get_solutions_to_problem'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK'){
          let num = 1;

          json.message.forEach((element: any) => {
            element.solutions.forEach((element2: any) => {
              this.solutions.push(new SolutionInfo(
                element2.code_ids, 
                element.title, 
                element2.solution_id,
                element2.author_id, 
                //@ts-ignore
                this.users_by_ids.get(element2.author_id).get_username(),
                element2.score,
                num))
                num++;
            });
          });
        }
      });

  }

  switchTab(name: string) {

    let i, tabcontent, tablinks;

    tabcontent = Array.from(document.getElementsByClassName('tabcontent') as HTMLCollectionOf<HTMLElement>);
    tablinks = document.getElementsByClassName("tablinks");

    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }

    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(name)!.style.display = "block";

  }

  show_invite_modal(): void{
    this.invite_modal.show();
  }

  send_group_invites(): void{
    const requestBody = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId(),
      group_id: this.group_id,
      invited_ids: this.users_to_invite
    };

    fetch((projectConfig.api_url + 'send_multiple_group_invites'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
        .then(response => response.json())
        .then(json => {
            this.success_modal_show(this.invite_modal, 'Успешно са изпратени поканите към потребителите.');
        });
  }

  show_ask_again_modal(ask_for: string, user_name: string, user_id: string): void
  {
    this.current_selected_user = user_id;
    switch(ask_for)
    {
      case 'become_admin':
        {
          this.current_clicked_option = 'become_admin';
          this.ask_again_message.innerHTML = "Сигурни ли сте че искате да направите <b>" + user_name + "</b> администратор?";
          break;
        }
      case 'revoke_admin':
        {
          this.current_clicked_option = 'revoke_admin';
          this.ask_again_message.innerHTML = "Сигурни ли сте че искате да премахнете администраторксите права на <b>" + user_name + "</b>?";
          break;
        }
      case 'remove_user':
        {
          this.current_clicked_option = 'remove_user';
          this.ask_again_message.innerHTML = "Сигурни ли сте че искате да премахнете <b>" + user_name + "</b> от групата?";
          break;
        }
    }
    this.ask_again_modal.show();
  }

  ask_again_button(): void{
    switch(this.current_clicked_option)
    {
      case 'become_admin':
        {
          this.make_user_admin();
          break;
        }
      case 'revoke_admin':
        {
          this.revoke_user_admin();
          break;
        }
      case 'remove_user':
        {
          this.remove_user();
          break;
        }
    }
  }

  make_user_admin(): void{
    const requestBody = {
      my_user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      user_id: this.current_selected_user,
      group_id: this.group_id
    }
    fetch((projectConfig.api_url + 'give_user_admin_access'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK'){
          this.success_modal_show(this.ask_again_modal, "Потребителят успешно е направен администратор.");
          this.cleanup_after_operation();

        }
        else{
          this.success_modal_show(this.ask_again_modal, "Възникна грешка.");
        }
      });
  }

  remove_user(): void{
    const requestBody = {
      my_user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      user_id: this.current_selected_user,
      group_id: this.group_id
    }
    fetch((projectConfig.api_url + 'kick_user_from_group'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK'){
          this.success_modal_show(this.ask_again_modal, "Потребителят успешно е премахнат от групата.");
          this.cleanup_after_operation();
        }
        else{
          this.success_modal_show(this.ask_again_modal, "Възникна грешка.");
        }
      });
  }

  revoke_user_admin(): void{
    const requestBody = {
      my_user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      user_id: this.current_selected_user,
      group_id: this.group_id
    }
    fetch((projectConfig.api_url + 'revoke_user_admin_access'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK'){
          this.success_modal_show(this.ask_again_modal, "Администраторските права на потребителя са премахнати успешно.");
          this.cleanup_after_operation();
        }
        else{
          this.success_modal_show(this.ask_again_modal, "Възникна грешка.");
        }
      });
  }

  cleanup_after_operation(): void{
    this.current_selected_user = '';
    this.current_clicked_option = '';
    this.get_group_info();
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

  success_modal_show(modal_to_hide: any, message_to_show: string)
  {
    modal_to_hide.hide();
    this.success_message.innerHTML = message_to_show;
    this.success_modal.show();
  }
}
