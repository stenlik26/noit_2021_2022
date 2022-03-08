import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
declare var Editor: any;
declare var MdFormatter: any;
declare var customTheme: any;
declare var sampleMarkdownText: any;
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';
import { TestField } from '../../solve_problem_test_field';
import { ProblemInformation } from 'src/app/problem_information';

@Component({
  selector: 'app-see-problem-page',
  templateUrl: './see-problem-page.component.html',
  styleUrls: ['./see-problem-page.component.scss']
})
export class SeeProblemPageComponent implements OnInit {

  problem_id: string = '';
  markdown_viewer: any;
  problem_title: any;
  problem_information: any;

  constructor(private activatedRoute: ActivatedRoute) { 
    //@ts-ignore
    this.problem_id = this.activatedRoute.snapshot.paramMap.get('id');

    if (typeof (this.problem_id) !== null)
      this.getProblemInfo(this.problem_id);
  }

  ngOnInit(): void {
    this.markdown_viewer = new Editor('editor', new MdFormatter(true), customTheme, true);
    this.markdown_viewer.setContent('# Зареждане <i class=\"fas fa-spinner fa-spin\"></i>');
  }

  getProblemInfo(id: string | null) {

    const requestBody = {
      problem_id: id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }

    fetch((projectConfig.api_url + 'get_problem_info'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => this.problem_info_output(json.message)
        .then(response => {
          this.problem_information = response;
          this.update_visual_elements();
        }));
  }

  async update_visual_elements() {
    console.log(this.problem_information);
    this.markdown_viewer.setContent(this.problem_information.get_problem_text());
    this.problem_title = document.getElementById('problem_title') as HTMLHeadingElement;
    this.problem_title.innerText = this.problem_information.get_problem_title();
  }

  async problem_info_output(json: any) {
    let problem_information = new ProblemInformation(
      json.start_date,
      json.end_date,
      json.text,
      json.time_limit,
      json.title);
    return problem_information;
  }


}
