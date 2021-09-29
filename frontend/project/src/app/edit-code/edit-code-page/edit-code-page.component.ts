import { Component, OnInit } from '@angular/core';
import {MonacoEditorModule} from "ngx-monaco-editor";
@Component({
  selector: 'app-edit-code-page',
  templateUrl: './edit-code-page.component.html',
  styleUrls: ['./edit-code-page.component.scss']
})
export class EditCodePageComponent implements OnInit {
  editorOptions = {theme: 'vs-dark', language: 'python'};
  code: string= '#include <iostream>\n\nint main() {\n\t//Program that prints "Hello world" to the console\n\tstd::cout<<"Hello world"<<std::endl;\n\treturn 0;\n}';
  editor = null;

  constructor() { }

  ngOnInit(): void {
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
    console.log(this.editor)
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
}
