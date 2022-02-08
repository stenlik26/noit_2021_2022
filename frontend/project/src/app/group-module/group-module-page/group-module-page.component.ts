import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';
import { ProblemInformationPick } from 'src/app/problem_info_pick';
import { UserInfo } from 'src/app/user_info';
import { SolutionInfo } from 'src/app/solution_info';

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

  async assign_group_info(data: any){
    this.group_title = data.name;
    let num = 1;

    data.problems.forEach((element: any) => {
      this.problems.push(new ProblemInformationPick(
        num,
        element.title,
        '-',
        [], 
        element._id.$oid, 
        element.start_date, 
        element.end_date, 
        element.is_active))
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

  ngOnInit(): void {
    this.switchTab('group_members');
    this.get_group_info();
    this.get_user_solutions();
  }

}
