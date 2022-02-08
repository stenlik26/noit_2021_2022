import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';
import { SubmissionInfo } from '../../submission_info';
import { MonacoEditorModule } from "ngx-monaco-editor";
import { Modal } from 'bootstrap';

@Component({
  selector: 'app-grade-solution-page',
  templateUrl: './grade-solution-page.component.html',
  styleUrls: ['./grade-solution-page.component.scss']
})
export class GradeSolutionPageComponent implements OnInit {

  solution_id: any;
  group_id: any;
  submissions: Array<SubmissionInfo> = new Array<SubmissionInfo>();
  current_submission: any;
  author_name: string = '';
  problem_name: string = '';
  editorOptions = { theme: 'vs-dark', language: '', readOnly: 'true' };
  code = '';
  editor = null;
  show_tests: boolean = true;
  test_tab_message: any;
  success_message: any;
  grade_modal: any;
  comment_modal: any;
  comment_posted: boolean = false;
  comment_body_1: any;
  comment_body_2: any;
  grade_body_1: any;
  grade_body_2: any;
  graded: boolean = false;

  constructor(private activatedRoute: ActivatedRoute) {
    this.solution_id = this.activatedRoute.snapshot.paramMap.get('solution_id');
    this.group_id = this.activatedRoute.snapshot.paramMap.get('group_id');
    this.check_for_access();
  }

  ngOnInit(): void {
    this.test_tab_message = document.getElementById('test_tab_message') as HTMLHeadingElement;
    this.success_message = document.getElementById('success_message') as HTMLParagraphElement;
    this.get_submissions();
    //@ts-ignore
    this.grade_modal = new Modal(document.getElementById('result_modal'));
    //@ts-ignore
    this.comment_modal = new Modal(document.getElementById('comment_modal'));
    this.comment_body_1 = document.getElementById('comment_body_1') as HTMLDivElement;
    this.comment_body_2 = document.getElementById('comment_body_2') as HTMLDivElement;
    this.grade_body_1 = document.getElementById('grade_body_1') as HTMLDivElement;
    this.grade_body_2 = document.getElementById('grade_body_2') as HTMLDivElement;

  }

  // @ts-ignore
  onInit(editor) {
    this.editor = editor;
    editor.getModel().setValue(this.current_submission.get_code());
    // @ts-ignore
    monaco.editor.setModelLanguage(this.editor.getModel(), this.current_submission.get_language());
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
        if (json.status === 'error_no_access') {
          window.location.href = projectConfig.site_url + 'not_found';
        }
      });
  }

  get_submissions(): void {
    const requestBody = {
      solution_id: this.solution_id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }
    fetch((projectConfig.api_url + 'get_problem_submissions'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if (json.status === 'OK') {
          json.message.forEach((element: any) => {
            this.submissions.push(new SubmissionInfo(element))
          });
          this.author_name = json.author_name;
          this.problem_name = json.problem_name;
          this.current_submission = this.submissions[0];

          this.update_tests();
          //@ts-ignore
          monaco.editor.setModelLanguage(this.editor.getModel(), this.current_submission.get_language());
          this.code = this.current_submission.get_code();


        }
        else {
          console.log('Възникна проблем', json);
        }
      });
  }

  update_tests(): void {
    this.test_tab_message.innerHTML = "Резултат от тестовете: " + this.current_submission.tests_passed + " / " + this.current_submission.tests_total;
    if (this.current_submission.tests_passed === this.current_submission.tests_total && this.current_submission.tests_total != undefined) {
      this.show_tests = false;
      this.success_message.style.display = 'block';
      this.success_message.style.margin = "1em";
    }
    else {
      this.show_tests = true;
      this.success_message.style.display = 'none';
    }
  }

  change_submission(): void {
    const selector = document.getElementById("submission_time") as HTMLSelectElement;
    this.current_submission = this.submissions[parseInt(selector.value)];
    //@ts-ignore
    monaco.editor.setModelLanguage(this.editor.getModel(), this.current_submission.get_language());
    this.code = this.current_submission.get_code();
    this.update_tests();
  }

  grade_problem(): void {
    this.comment_body_1.style.display = "block";
    this.comment_body_2.style.display = "none";
    this.graded = false;
    this.grade_modal.show();
  }

  comment_problem(): void {
    this.grade_body_1.style.display = "block";
    this.grade_body_2.style.display = "none";
    this.comment_posted = false;
    this.comment_modal.show();
  }

  set_comment_to_problem(): void {

    const comment = (document.getElementById('comment') as HTMLTextAreaElement).value;

    const requestBody = {
      solution_id: this.solution_id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      comment: comment
    }
    fetch((projectConfig.api_url + 'set_comment_to_solution'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if (json.status === 'OK') {
          this.comment_body_1.style.display = "none";
          this.comment_body_2.style.display = "block";
          this.comment_posted = true;
        }
      });
  }

  set_solution_grade(): void {
    const grade = (document.getElementById('grade') as HTMLSelectElement).value;

    const requestBody = {
      solution_id: this.solution_id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      grade: grade
    }
    fetch((projectConfig.api_url + 'grade_solution'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if (json.status === 'OK') {
          this.grade_body_1.style.display = "none";
          this.grade_body_2.style.display = "block";
          this.graded = true;
        }
      });
  }

  goto_groups(): void {
    window.location.href = projectConfig.site_url + 'group/' + this.group_id;
  }
}

