import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {Toast} from "bootstrap";
import {ProblemInformation} from "../../problem_information";
import {UserTokenHandling} from "../../user_token_handling";
import projectConfig from "../../../assets/conf.json";
import { Octokit } from 'octokit';
import { Modal } from 'bootstrap';

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
  github_gist_modal: any;
  has_github_token: boolean = false;
  github_token: string = "";
  should_wait: boolean = false;

  language_extention: {[name: string]:string} = {
    "java": ".java",
    "python": ".py",
    "cpp": ".cpp",
    "js": ".js",
    "c": ".c"

  }


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
    //@ts-ignore
    this.github_gist_modal = new Modal(document.getElementById("github_gist_modal"));

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

  async create_github_gist(){
      //@ts-ignore
      const content = this.editor.getValue();

      const filename_field: HTMLInputElement = document.getElementById("filename_input") as HTMLInputElement;
      let filename = filename_field.value;
  
      if(filename === "" || filename === null)
      {
        filename = "code" + Date.now();
      }
  
      filename += this.language_extention[this.getLanguageFromSelect()];

      console.log(filename);
      
      const octokit = new Octokit({
        auth: this.github_token
      })

      const description_Text = (document.getElementById("github_desc") as HTMLTextAreaElement).value;

      const is_public = (document.getElementById("public_checkbox") as HTMLInputElement).checked;

      this.should_wait = true;


      const resp = await octokit.request("POST /gists", {
        files:{
          [filename]: {"content": content}
        },
        description: description_Text,
        public: is_public
      })

      window.open(resp.data.html_url);
      
      (document.getElementById("wait_text") as HTMLParagraphElement).textContent = "Кодът е успешно качен в Github Gists.";

  }

  show_github_gist_modal(): void
  {
    this.should_wait = false;
    const requestBody = {
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken()
    }
    
    fetch((projectConfig.api_url + 'get_github_token'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if(json.status === 'OK')
        {
          if(json.message != "-1")
          {
            this.has_github_token = true;
            this.github_token = json.message;
          }
          else{
            this.has_github_token = false;
            this.github_token = "";
          }
        } 
      });


    this.github_gist_modal.show();
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

    if(filename === "" || filename === null)
    {
      filename = "code";
    }

    filename += this.language_extention[this.getLanguageFromSelect()];

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
