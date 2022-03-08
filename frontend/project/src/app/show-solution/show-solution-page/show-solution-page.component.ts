import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';
import { SubmissionInfo } from 'src/app/submission_info';
import { MonacoEditorModule } from "ngx-monaco-editor";
import { Modal } from 'bootstrap';

@Component({
  selector: 'app-show-solution-page',
  templateUrl: './show-solution-page.component.html',
  styleUrls: ['./show-solution-page.component.scss']
})
export class ShowSolutionPageComponent implements OnInit {

  code_id: string = '';
  current_code: SubmissionInfo = null!;
  problem_title: string = '';
  editorOptions = { theme: 'vs-dark', language: '', readOnly: 'true' };
  code = '';
  editor = null;
  show_tests: boolean = true;
  test_tab_message: any;
  success_message: any;
  author_name: string = '';
  access: boolean = false;
  problem_public: boolean = false;
  share_modal: any;
  problem_shared: boolean = false;
  error_occured: boolean = false;
  comments_modal: any;
  is_code_playground: boolean = false;

  constructor(private activatedRoute: ActivatedRoute) {
    if (!UserTokenHandling.isUserLoggedIn()) {
      window.location.href = projectConfig.site_url + 'not_found';
    }
    //@ts-ignore
    this.code_id = this.activatedRoute.snapshot.paramMap.get('code_id');
  }

  ngOnInit(): void {
    this.get_code_info();
    this.success_message = document.getElementById('success_message') as HTMLParagraphElement;
    this.test_tab_message = document.getElementById('test_tab_message2') as HTMLHeadingElement;
    //@ts-ignore
    this.share_modal = new Modal(document.getElementById('share_modal'));
    //@ts-ignore
    this.comments_modal = new Modal(document.getElementById('comments_modal'));
  }

  // @ts-ignore
  onInit(editor) {
    this.editor = editor;
    editor.getModel().setValue(this.current_code.get_code());
    // @ts-ignore
    monaco.editor.setModelLanguage(this.editor.getModel(), this.current_code.get_language());
  }

  show_share_modal(): void {
    this.share_modal.show();
  }

  show_comments_modal(): void {
    this.comments_modal.show();
  }

  get_code_info(): void {
    const requestBody = {
      code_id: this.code_id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }
    fetch((projectConfig.api_url + 'get_code_info'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
 
        this.current_code = new SubmissionInfo(json.message);

        this.problem_title = json.message.problem_name;

        this.author_name = json.message.author_name;
        this.access = (UserTokenHandling.getUserId() === json.message.author_id.$oid);
        this.problem_public = json.message.problem_public;
        this.problem_shared = json.message.shared;

        if (json.status === 'OK') {
          if (!json.message.hasOwnProperty('name')) {
            this.is_code_playground = false;
            this.update_tests();
          }
          else{
            this.is_code_playground = true;
            (document.getElementById('problem_tests') as HTMLDivElement).style.display = 'none';
          }

        }
        else if (json.status === 'error_no_access') {
          window.location.href = projectConfig.site_url + 'not_found';
        }
      });
  }

  update_tests(): void {
    this.test_tab_message.innerHTML = "Резултат от тестовете: " + this.current_code.tests_passed + " / " + this.current_code.tests_total;
    if (this.current_code.tests_passed === this.current_code.tests_total && this.current_code.tests_total != undefined) {
      this.show_tests = false;
      this.success_message.style.display = 'block';
      this.success_message.style.margin = "1em";
    }
    else {
      this.show_tests = true;
      this.success_message.style.display = 'none';
    }
  }

  share_solution(): void {
    if (this.problem_shared) {
      return;
    }

    const requestBody = {
      code_id: this.code_id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }
    fetch((projectConfig.api_url + 'share_solution'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if (json.status === 'OK') {
          this.problem_shared = true;
        }
        else {
          this.error_occured = true;
        }
      });
  }

}
