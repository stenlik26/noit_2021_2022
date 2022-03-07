import { Component, OnInit } from '@angular/core';
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';
import { ProblemInformationPick } from 'src/app/problem_info_pick';

@Component({
  selector: 'app-show-problems-page',
  templateUrl: './show-problems-page.component.html',
  styleUrls: ['./show-problems-page.component.scss']
})
export class ShowProblemsPageComponent implements OnInit {

  constructor() { 
    this.not_logged_in = !UserTokenHandling.isUserLoggedIn();
  }

  problems: Array<ProblemInformationPick> = new Array<ProblemInformationPick>();
  current_difficulty: string = 'any';
  current_tags: string = 'any';
  current_search_name: string = '';
  show_solve: boolean = true;
  name_input: any;
  not_logged_in: boolean = false;

  get_problems(): void{

    const requestBody = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId(),
      difficulty: this.current_difficulty,
      tags: this.current_tags,
      name: this.current_search_name
    };

    fetch((projectConfig.api_url + 'get_all_problems'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status != 'OK')
        {
          return;
        }
        let num = 1;
        json.message.forEach((element: any) => {
          this.problems.push(new ProblemInformationPick(num, element.title, element.difficulty, element.tags, element._id))
          num++;
        });
        this.show_solve = true;
        if(num === 1)
        {
          this.problems.push(new ProblemInformationPick(0, 'Няма намерени задачи с избраните филтри.', '-', [], ''))
          this.show_solve = false;
        }
        
      });
  }

  change_difficulty(): void{
    const selector = document.getElementById("difficulty_selector_box") as HTMLSelectElement;
    this.current_difficulty = selector.value;
    this.problems = [];
    this.get_problems();
  }

  change_tags(): void{
    const selector = document.getElementById("tags_selector_box") as HTMLSelectElement;
    this.current_tags = selector.value;
    this.problems = [];
    this.get_problems();
  }

  search_by_name(): void{
    this.current_search_name = this.name_input.value;
    this.problems = [];
    this.get_problems();
  }

  ngOnInit(): void {

    this.name_input = document.getElementById("problem_name") as HTMLInputElement;

    if (!UserTokenHandling.isUserTokenSet) {
      UserTokenHandling.setGuestToken();
    }
    this.get_problems();
  }

}
