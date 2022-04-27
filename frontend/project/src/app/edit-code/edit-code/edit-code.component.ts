import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {Toast} from "bootstrap";
import {ProblemInformation} from "../../problem_information";
import {UserTokenHandling} from "../../user_token_handling";
import projectConfig from "../../../assets/conf.json";

@Component({
  selector: 'app-edit-code',
  templateUrl: './edit-code.component.html',
  styleUrls: ['./edit-code.component.scss']
})
export class EditCodeComponent implements OnInit {
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


  constructor(private activatedRoute: ActivatedRoute) {
    this.problem_id = this.activatedRoute.snapshot.paramMap.get('id');

    if (this.problem_id != null) {
      this.load_code();
    }
  }

  ngOnInit(): void {
    this.toast_content = document.getElementById('toast_content') as HTMLParagraphElement;
    this.toastEl = document.getElementById('liveToast');
    console.log(this.toastEl);
    //@ts-ignore
    this.toast = new Toast(this.toastEl);
    console.log(this.toast);
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

    if (apiStatus.status === 'OK')
    {
      stdout_area.value = apiStatus.message.stdout + "\n" + apiStatus.message.stderr;
    }
    else{
      stdout_area.value = "Грешка при заявката";
    }
  }

  showToast(message: string){

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
  executeCode(): void {
    const language: string = this.getLanguageFromSelect();
    // @ts-ignore
    const current_code = this.editor.getValue();

    const stdin_box = document.getElementById("stdin") as HTMLTextAreaElement;

    let requestBody = null;

    if (stdin_box.value != '') {
      requestBody = {
        user_id: 1,
        code: current_code,
        language: language,
        token: "foobarbaz",
        stdin: stdin_box.value
      };
    }
    else {
      requestBody = {
        user_id: 1,
        code: current_code,
        language: language,
        token: "foobarbaz"
      };
    }

    fetch(('http://ec2-3-125-7-165.eu-central-1.compute.amazonaws.com/run_test'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => this.handleOutput(json));
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

  download_code()
  {
    //@ts-ignore
    const content = this.editor.getValue();

    const filename_field: HTMLInputElement = document.getElementById("filename_input") as HTMLInputElement;
    let filename = filename_field.value;

    switch(this.getLanguageFromSelect())
    {
      case "cpp":
        {
          filename += ".cpp";
          break;
        }
      case "java":{
        filename += ".java";
        break;
      }
      case "python":{
        filename += ".py";
        break;
      }
    }

    const element = document.createElement('a');

    const blob = new Blob([content], { type: 'plain/text' });

    const fileUrl = URL.createObjectURL(blob);
    
    element.setAttribute('href', fileUrl);
    element.setAttribute('download', filename);
    element.style.display = 'none';
    
    document.body.appendChild(element);
    element.click();
    
    document.body.removeChild(element);
  }


  upload_code_output(json: any)
  {
    this.showToast("Вашето решение е качено успешно.");
    console.log(json);
  }

  upload_code(message: string) {
    this.showToast(message);
    // @ts-ignore
    const current_code = this.editor.getValue();
    const filename_field: HTMLInputElement = document.getElementById("filename_input") as HTMLInputElement;
    const filename = filename_field.value;
    const requestBody = {
      problem_id: this.problem_id,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      language: this.getLanguageFromSelect(),
      name: filename,
      code: current_code
    }

    fetch((projectConfig.api_url + 'upload_codeplayground'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => this.upload_code_output(json.message));
  }

  private load_code() {
    console.log("Problem_id = ", this.problem_id);

    let requestBody = {
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      code_id: this.problem_id
    };

    fetch((projectConfig.api_url + 'get_codeplayground'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {

        if(json.status !== undefined)
        {
          window.location.href = projectConfig.site_url + 'not_found';
        }
        const filename_field: HTMLInputElement = document.getElementById("filename_input") as HTMLInputElement;
        filename_field.value = json.name;
        const selector = document.getElementById("language-selector") as HTMLSelectElement;
        selector.value = json.language;

        this.code = json.code;
        // @ts-ignore
        monaco.editor.setModelLanguage(this.editor.getModel(), json.language);

      });
  }
}
