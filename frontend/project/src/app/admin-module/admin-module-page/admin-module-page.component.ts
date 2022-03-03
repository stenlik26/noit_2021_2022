import { Component, OnInit } from '@angular/core';
import { UserTokenHandling } from 'src/app/user_token_handling';
import projectConfig from '../../../assets/conf.json';
import { UserInfo } from 'src/app/user_info';
import { UnapprovedPicture } from '../UnapprovedPicture';
import { AdminGroupInfo } from '../AdminGroupInfo';

@Component({
  selector: 'app-admin-module-page',
  templateUrl: './admin-module-page.component.html',
  styleUrls: ['./admin-module-page.component.scss']
})
export class AdminModulePageComponent implements OnInit {

  constructor() { }

  admin_panel: HTMLDivElement = null!;
  deny_access_panel: HTMLDivElement = null!;
  wait_panel: HTMLDivElement = null!;
  users: Array<UserInfo> = new Array<UserInfo>();
  unapproved_pictures: Array<UnapprovedPicture> = new Array<UnapprovedPicture>();
  groups: Array<AdminGroupInfo> = new Array<AdminGroupInfo>();

  ngOnInit(): void {
    this.admin_panel = document.getElementById('adminPanel') as HTMLDivElement;
    this.deny_access_panel = document.getElementById('adminPanelNoAccess') as HTMLDivElement;
    this.wait_panel = document.getElementById('adminPanelWait') as HTMLDivElement;
    this.authUser();
    this.switchTab('usersList');
  }

  authUser(): void
  {
    const data = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId()
    };

    fetch(projectConfig.api_url + 'has_access_to_admin_panel', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-type': 'application/json' }
    }).then(response => response.json()).then(json => {
      console.log(json);
      if (json.status === 'OK') {
        this.showAdminPanel();
      }
      else {
        this.denyAccess();
      }
    });
  }

  load_admin_info(): void{

    this.unapproved_pictures = [];
    this.users = [];
    this.groups = [];

    const data = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId()
    };

    fetch(projectConfig.api_url + 'get_admin_panel_info', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-type': 'application/json' }
    }).then(response => response.json()).then(json => {
      console.log(json);
      if (json.status === 'OK') {
        json.users.forEach((element: any) => {
          this.users.push(new UserInfo(element));
        });

        json.pictures.forEach((element: any) => {
          this.unapproved_pictures.push(new UnapprovedPicture(
            element._id.$oid,
            element.user_name,
            element.path_Full,
            element.time))
        });

        json.groups.forEach((element: any) => {
          this.groups.push(new AdminGroupInfo(element));
        });
        console.log(this.unapproved_pictures);
        console.log(this.users);
        console.log(this.groups);
      }
    });
  }
  
  showAdminPanel(): void
  {
    this.wait_panel.style.display = 'none';
    this.admin_panel.style.display = 'grid';
    this.load_admin_info();
  }

  denyAccess(): void
  {
    this.wait_panel.style.display = 'none';
    this.deny_access_panel.style.display = 'grid';
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

    document.getElementById(name)!.style.display = "block";

  }

  
  approvePic(imageIdArg: string): void
  {
    /*
    const data = {
      token: UserTokenHandling.getUserToken(),
      userId: UserTokenHandling.getUserId(),
      pictureId: imageIdArg
    };
    console.log(data);

    fetch(conf.url + 'approveUploadedPicture', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-type': 'application/json' }
    }).then(response => response.json()).then(json => {
      console.log(json);
      if (json.status === 'OK') {
        alert('Снимката е успешно качена.');
        location.reload();
      }
      else {
        console.log(json.message);
      }
    });
    */
  }

  viewImage(pic: UnapprovedPicture): void{
    /*
    let path = pic.getPicPath();
    path = path.replace('\\', '/');
    window.open(path);
    */
  }

  deleteImage(imageIdArg: string): void{
    /*
    const data = {
      token: UserTokenHandling.getUserToken(),
      userId: UserTokenHandling.getUserId(),
      pictureId: imageIdArg
    };
    console.log(data);

    fetch(conf.url + 'deleteUnapprovedPicture', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-type': 'application/json' }
    }).then(response => response.json()).then(json => {
      console.log(json);
      if (json.status === 'OK') {
        alert('Снимката е успешно премахната.');
        location.reload();
      }
      else {
        console.log(json.message);
      }
    });
    */
  }

  make_user_admin(user_to_make_id: string): void{
    const data = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId(),
      to_set_user_id: user_to_make_id
    };

    fetch(projectConfig.api_url + 'make_user_admin_on_site', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-type': 'application/json' }
    }).then(response => response.json()).then(json => {
      console.log(json);
      if (json.status === 'OK') {
        this.load_admin_info();
      }
      else{
        console.log(json);
      }
    });
  }

  revoke_user_admin(user_to_make_id: string): void{
    const data = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId(),
      to_set_user_id: user_to_make_id
    };

    fetch(projectConfig.api_url + 'revoke_user_admin_on_site', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-type': 'application/json' }
    }).then(response => response.json()).then(json => {
      console.log(json);
      if (json.status === 'OK') {
        this.load_admin_info();
      }
      else{
        console.log(json);
      }
    });

  }

  delete_group(group_id: string): void{
    const data = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId(),
      group_id: group_id
    };

    fetch(projectConfig.api_url + 'delete_group', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-type': 'application/json' }
    }).then(response => response.json()).then(json => {
      console.log(json);
      if (json.status === 'OK') {
        this.load_admin_info();
      }
      else{
        console.log(json);
      }
    });
  }
}

