import { Component, OnInit } from '@angular/core';
import bootstrap from 'bootstrap';
import projectConfig from '../../../assets/conf.json'

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss']
})
export class HomePageComponent implements OnInit {

  constructor() { }

  active_problems: number = 0;

  ngOnInit(): void {
    this.get_active_problems();
  }

  get_active_problems(): void{
    fetch((projectConfig.api_url + 'get_number_of_tasks'), {
      method: 'GET',
      headers: { 'Content-type': 'application/json' }
    })
      .then(response => response.json())
      .then(json => {
        this.active_problems = json.message;
      });
  }
}
