import { Component, OnInit } from '@angular/core';
import {editor} from "monaco-editor";

@Component({
  selector: 'app-editor',
  templateUrl: './editor.component.html',
  styleUrls: ['./editor.component.scss']
})
export class EditorComponent implements OnInit {

  editorOptions = {theme: 'vs-dark', language: 'cpp'};
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

  executeCode(): void {
    console.log("Clicked");
    // @ts-ignore
    console.log(this.editor.getValue());
  }
}
