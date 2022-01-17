import { Component, OnInit } from '@angular/core';
import { MonacoEditorModule } from "ngx-monaco-editor";
import { ActivatedRoute } from '@angular/router';
declare var Editor: any;
declare var MdFormatter: any;
declare var customTheme: any;
declare var sampleMarkdownText: any;
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';
import { TestField } from '../../solve_problem_test_field';
import { ProblemInformation } from 'src/app/problem_information';
import { Toast } from 'bootstrap';

@Component({
  selector: 'app-edit-code-page',
  templateUrl: './edit-code-page.component.html',
  styleUrls: ['./edit-code-page.component.scss']
})
export class EditCodePageComponent implements OnInit {
  editorOptions = { theme: 'vs-dark', language: 'cpp' };
  code: string = '#include <iostream>\n\nint main() {\n\t//Program that prints "Hello world" to the console\n\tstd::cout<<"Hello world"<<std::endl;\n\treturn 0;\n}';
  editor = null;
  markdown_viewer: any;
  problem_title: any;
  problem_information: any;
  problem_id: any;
  toast: any;
  toastEl: any;
  toast_content: any;
  total_tests: number = 0;
  total_passed: number = 0;
  show_tests: boolean = false;
  test_tab_message: any;
  error_textarea: any;
  success_message: any;



  constructor(private activatedRoute: ActivatedRoute) {
    this.problem_id = this.activatedRoute.snapshot.paramMap.get('id');

    this.check_for_access();

    if (typeof (this.problem_id) !== null)
      this.getProblemInfo(this.problem_id);

  }

  check_for_access(): void{
    const requestBody = {
      problem_id: this.problem_id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }
    fetch(('http://127.0.0.1:5100/user_access_to_problem'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.has_access === false)
        {
          window.location.href = projectConfig.site_url + 'not_found';
        }
      });
  }
  ngOnInit(): void {

    this.markdown_viewer = new Editor('editor', new MdFormatter(true), customTheme, true);
    this.markdown_viewer.setContent('# Зареждане <i class=\"fas fa-spinner fa-spin\"></i>');
    this.toast_content = document.getElementById('toast_content') as HTMLParagraphElement;
    this.test_tab_message = document.getElementById('test_tab_message') as HTMLHeadingElement;
    this.toastEl = document.getElementById('liveToast');
    this.error_textarea = document.getElementById('error_textarea') as HTMLTextAreaElement;
    this.success_message = document.getElementById('success_message') as HTMLParagraphElement;
    //@ts-ignore
    this.toast = new Toast(this.toastEl);
  }

  // @ts-ignore
  onInit(editor) {
    this.editor = editor;
  }

  public getCode(): string {
    // @ts-ignore
    return this.editor.getValue();
  }

  async handleOutput(apiStatus: { status: any; message: { stdout: string; stderr: string; }; }): Promise<void> {
    const stdout_area = document.getElementById('stdout') as HTMLTextAreaElement;
    const stderr_area = document.getElementById('stderr') as HTMLTextAreaElement;

    if (apiStatus.status === 'OK') {
      stdout_area.value = apiStatus.message.stdout;
      stderr_area.value = apiStatus.message.stderr;
    }
    else {
      stdout_area.value = "Грешка при заявката";
    }
  }

  showToast(message: string) {

    this.toast_content.innerHTML = message;
    //@ts-ignore
    this.toast.show();
  }

  changeLanguageSelect() {
    // @ts-ignore
    monaco.editor.setModelLanguage(this.editor.getModel(), this.getLanguageFromSelect());
  }
  getLanguageFromSelect(): string {
    const selector = document.getElementById("language-selector") as HTMLSelectElement;
    return selector.value;
  }
  /*
  executeCode(): void {
    const language: string = this.getLanguageFromSelect();
    // @ts-ignore
    const current_code = this.editor.getValue();

    const requestBody = {
      user_id: 1,
      code: current_code,
      language: language,
      token: UserTokenHandling.getUserToken(),

    };

    fetch(('http://127.0.0.1:5100/run_code'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => this.handleOutput(json));
  }
*/
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

    if (name === "problem_options") {
      document.getElementById(name)!.style.display = "flex";
    }
    else {
      document.getElementById(name)!.style.display = "block";
    }

    //evt.currentTarget!.className += " active";
  }

  run_tests() {
    this.switchTab('problem_tests');
    this.test_tab_message.innerHTML = "Моля изчакайте <i class=\"fas fa-spinner fa-spin\"></i>";
    this.success_message.style.display = 'none';
    this.error_textarea.style.display = "none";
    this.show_tests = false;
    //@ts-ignore
    const current_code = this.editor.getValue();

    const requestBody = {
      problem_id: this.problem_id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      language: this.getLanguageFromSelect(),
      code: current_code
    }
    fetch((projectConfig.api_url + 'run_problem_tests'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => this.run_tests_output(json));
  }

  run_tests_output(json: any) {

    if (json.status != 'OK') {

      switch (json.status) {

        case 'error_executor':
          {
            console.log("Error from API. - " + json.status + " - " + json.message);
            this.show_tests = false;
            return;
            
          }

        case 'error_compile':
          {
            this.test_tab_message.innerHTML = "Грешка при изпълнение:";
            this.error_textarea.style.display = "block";
            this.error_textarea.innerText = json.message;
            this.show_tests = false;
            return;
          }

      }

    }

    json = json.message;
    this.total_passed = json.passed;
    this.total_tests = json.total;
    this.problem_information.test_fields = [];
    this.test_tab_message.innerHTML = "Резултат от тестовете: " + this.total_passed + " / " + this.total_tests;

    if(this.total_passed === this.total_tests && this.total_tests != undefined)
    {
      this.show_tests = false;
      this.success_message.style.display = 'block';
      this.success_message.style.margin = "1em";
    }
    else{
      this.success_message.style.display = 'none';
    }


    if (json.results.length != 0) {

      let id = 1;
      json.results.forEach((element: any) => {
        
        
        this.problem_information.test_fields.push(new TestField(
          id.toString(),
          element.input,
          element.test_output,
          element.expected_stdout,
          element.diff,
          0));
        id++;
      });

      this.show_tests = true;

    }
    

  }

  async problem_info_output(json: any) {
    console.log(json);
    let problem_information = new ProblemInformation(
      json.start_date,
      json.end_date,
      json.text,
      json.time_limit,
      json.title);
    return problem_information;
  }

  async update_visual_elements() {
    this.markdown_viewer.setContent(this.problem_information.get_problem_text());
    this.problem_title = document.getElementById('problem_title') as HTMLHeadingElement;
    this.problem_title.innerText = this.problem_information.get_problem_title();
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

  upload_code_output(json: any) {
    this.showToast("Вашето решение е качено успешно.");
    console.log(json);
  }

  upload_code(message: string) {
    this.showToast(message);
    // @ts-ignore
    const current_code = this.editor.getValue();

    const requestBody = {
      problem_id: this.problem_id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      language: this.getLanguageFromSelect(),
      code: current_code
    }

    fetch((projectConfig.api_url + 'upload_code'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => this.upload_code_output(json.message));
  }
}
