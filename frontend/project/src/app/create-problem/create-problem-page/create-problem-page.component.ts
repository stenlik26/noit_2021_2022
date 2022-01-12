import { Component, OnInit } from '@angular/core';
import { TestField } from '../../create_problem_test_field';
declare var Editor: any;
declare var MdFormatter: any;
declare var customTheme: any;
declare var sampleMarkdownText: any;
import { UserTokenHandling } from 'src/app/user_token_handling';
import projectConfig from '../../../assets/conf.json'
import { Modal } from 'bootstrap';

@Component({
  selector: 'app-create-problem-page',
  templateUrl: './create-problem-page.component.html',
  styleUrls: ['./create-problem-page.component.scss']
})
export class CreateProblemPageComponent implements OnInit {

  constructor() {
  }

  test_fields: Array<TestField> = new Array<TestField>();
  editor: any;
  modal: Modal = new Modal('');
  problem_created: boolean = false;
  modal_content: any;
  groups: Array<any> = new Array<any>();
  select_groups: boolean = false;

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

  access_change(event: any) {
    this.select_groups = (event.target.value == 'by_groups');
  }

  create_problem(): void {
    const problem_text: string = this.editor.getContent();
    const title: string = (document.getElementById('problem_title_input') as HTMLInputElement).value;
    const problem_access: HTMLSelectElement = (document.getElementById('access') as HTMLSelectElement);
    const time_limit: string = (document.getElementById('problem_time_limit') as HTMLInputElement).value;
    const start_date: string = (document.getElementById('problem_start_date') as HTMLInputElement).value;
    const end_date: string = (document.getElementById('problem_end_date') as HTMLInputElement).value;
    const tags: string = (document.getElementById('problem_tags') as HTMLInputElement).value;
    const difficulty: string = (document.getElementById('difficulty') as HTMLInputElement).value;

    this.update_test_array();

    this.modal_content.innerHTML = "Моля изчакайте..."
    this.modal.show();

    let access = problem_access.value === "public" ? "true" : "false";
    let groups_to_add_problem: Array<String> = new Array<String>();

    let selected_groups = document.getElementById('groups') as HTMLSelectElement;
    if (selected_groups != null) {
      for (let i = 0; i < selected_groups.selectedOptions.length; i++) {
        groups_to_add_problem.push(selected_groups.selectedOptions[i].value);
      }
    }
    const requestBody = {
      title: title,
      text: problem_text,
      public: access,
      time_limit: time_limit,
      start_date: start_date,
      end_date: end_date,
      tests: JSON.stringify(this.test_fields, ["input", "output", "is_hidden", "time_limit"]),
      tags: tags,
      user_id: UserTokenHandling.getUserId(),
      token: UserTokenHandling.getUserToken(),
      difficulty: difficulty,
      groups_to_add_problem: groups_to_add_problem
    }


    fetch((projectConfig.api_url + 'create_problem'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        if (json.status == "OK") {
          this.problem_created = true;
          this.modal_content.innerHTML = "Задачата е успешно създадена."
          this.modal.show();
        }
        else {
          this.modal_content.innerHTML = "Моля попълнете всички полета."
          this.modal.show();
        }
      });
  }

  go_to_main_page(): void {
    window.location.href = projectConfig.site_url;
  }

  update_test_array(): void {
    let input: string;
    let output: string;
    let time_limit: string;
    let is_hidden: boolean;

    for (let i = 1; i <= this.test_fields.length; i++) {
      input = (document.getElementById('test_input_field_' + i.toString()) as HTMLTextAreaElement).value;
      output = (document.getElementById('test_output_field_' + i.toString()) as HTMLTextAreaElement).value;
      time_limit = (document.getElementById('test_time_limit_input_' + i.toString()) as HTMLInputElement).value;
      is_hidden = (document.getElementById('is_test_hidden_' + i.toString()) as HTMLInputElement).checked;
      this.test_fields[i - 1].setTest(input, output, is_hidden, time_limit);
    }
  }

  add_test_field(): void {
    this.test_fields.push(new TestField((this.test_fields.length + 1).toString(), '', '', false, ''))
  }

  remove_test_field(test_field: any): void {
    let index_to_delete = 0;
    let test_num_to_delete = test_field.get_test_num();

    for (let i = 0; i < this.test_fields.length; i++) {
      if (this.test_fields[i].get_test_num() === test_num_to_delete) {
        index_to_delete = i;
        break;
      }
    }
    this.test_fields.splice(index_to_delete, 1);
  }
  get_groups_where_user_is_admin(): void {
    const requestBody = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId()
    };

    fetch((projectConfig.api_url + 'get_groups_user_admin'), {
      method: 'POST',
      body: JSON.stringify(requestBody),
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        this.groups = json;
      });
  }

  ngOnInit(): void {

    // Обясненеие за аргументите:
    // 'editor' - id-то на div елемента в html страницата
    // MdFormatter - създава се нов клас като изисква атрибут за режим на редактора. (Прочети последното)
    // customTheme - Темата на полето за условието (тема на scrollbar, тема на редактора, други css настройки и т.н.)
    // Последният атрибут false или ture е затова дали редактора е във read-only режим. Ако е false, може да се пише в редактора, ако е true, може само да се чете от редактора.
    this.editor = new Editor('editor', new MdFormatter(false), customTheme, false);
    this.editor.setContent(sampleMarkdownText);
    this.editor.setContentBasic();

    this.test_fields.push(new TestField((this.test_fields.length + 1).toString(), '', '', false, ''))

    if (!UserTokenHandling.isUserTokenSet) {
      UserTokenHandling.setGuestToken();
    }
    this.switchTab('problem_text_editor');
    //@ts-ignore
    this.modal = new Modal(document.getElementById('result_modal'));
    this.modal_content = document.getElementById('modal_content') as HTMLParagraphElement;
    this.get_groups_where_user_is_admin();
  }

}
