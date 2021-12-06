import { Component, OnInit } from '@angular/core';
import {MonacoEditorModule} from "ngx-monaco-editor";
import { ActivatedRoute } from '@angular/router';
declare var Editor: any;
declare var MdFormatter: any;
declare var customTheme: any;
declare var sampleMarkdownText: any;
import projectConfig from '../../../assets/conf.json'
import { UserTokenHandling } from 'src/app/user_token_handling';
import { TestField } from '../../create_problem_test_field'; 
import { ProblemInformation } from 'src/app/problem_information';

@Component({
  selector: 'app-edit-code-page',
  templateUrl: './edit-code-page.component.html',
  styleUrls: ['./edit-code-page.component.scss']
})
export class EditCodePageComponent implements OnInit {
  editorOptions = {theme: 'vs-dark', language: 'cpp'};
  code: string= '#include <iostream>\n\nint main() {\n\t//Program that prints "Hello world" to the console\n\tstd::cout<<"Hello world"<<std::endl;\n\treturn 0;\n}';
  editor = null;
  markdown_viewer: any;

  problem_information: any;


  constructor(private activatedRoute: ActivatedRoute) { 
    let id = this.activatedRoute.snapshot.paramMap.get('id');

    if(typeof(id) !== null)
      this.getProblemInfo(id);

  }

  ngOnInit(): void {
    this.markdown_viewer = new Editor('editor', new MdFormatter(true), customTheme, true);
    this.markdown_viewer.setContent('# Зареждане...');

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

    console.log(apiStatus.status);
    console.log(apiStatus);

    switch (apiStatus.status)
    {
      case 'OK':
      {
        stdout_area.value = apiStatus.message.stdout;
        stderr_area.value = apiStatus.message.stderr;
        break;
      }
      default:
      {
        stdout_area.value = "Грешка при заявката";
        break;
      }
    }
  }

  changeLanguageSelect() {
    // @ts-ignore
    monaco.editor.setModelLanguage(this.editor.getModel(), this.getLanguageFromSelect());
  }
  getLanguageFromSelect(): string {
    const selector = document.getElementById("language-selector") as HTMLSelectElement;
    return selector.value;
  }
  executeCode(): void {
    console.log("Clicked");
    const language: string = this.getLanguageFromSelect();
    // @ts-ignore
    const current_code = this.editor.getValue();

    const requestBody = {
      user_id: 1,
      code: current_code,
      language: language,
      token: "foobarbaz"
    };

    fetch(('http://127.0.0.1:5100/run_code'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => this.handleOutput(json));
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

    if (name === "problem_options") {
      document.getElementById(name)!.style.display = "flex";
    }
    else {
      document.getElementById(name)!.style.display = "block";
    }

    //evt.currentTarget!.className += " active";
  }

  async problem_info_output(json: any)
  {
    let problem_information = new ProblemInformation(json.start_date, json.end_date, json.text, json.time_limit);
    let id = 1;
    json.tests.forEach((element: any) => {
      problem_information.test_fields.push(new TestField(
      id.toString(), 
      element.input, 
      element.output, 
      element.is_hidden, 
      element.time_limit));
        id++;
    });
    return problem_information;
  }

  async update_visual_elements()
  {
    this.markdown_viewer.setContent(this.problem_information.get_problem_text());
  }

  getProblemInfo(id: string | null){

    const requestBody = {
      problem_id: id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }

    fetch((projectConfig.api_url + ''), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => this.problem_info_output(json)
      .then(response =>  {
        this.problem_information = response;
        this.update_visual_elements();
      }));
  }
}
