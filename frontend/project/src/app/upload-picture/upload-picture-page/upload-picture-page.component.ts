import { Component, OnInit } from '@angular/core';
import { UserTokenHandling } from 'src/app/user_token_handling';
import projectConfig from '../../../assets/conf.json'

@Component({
  selector: 'app-upload-picture-page',
  templateUrl: './upload-picture-page.component.html',
  styleUrls: ['./upload-picture-page.component.scss']
})
export class UploadPicturePageComponent implements OnInit {

  constructor() { }

  image: string | Blob = '';
  mainPanel: HTMLDivElement = null!;
  waitPanel: HTMLDivElement = null!;
  donePanel: HTMLDivElement = null!;
  errorPanel: HTMLDivElement = null!;

  ngOnInit(): void {
    this.waitPanel = document.getElementById('uploadProfilePicWait') as HTMLDivElement;
    this.donePanel = document.getElementById('uploadProfilePicDone') as HTMLDivElement;
    this.mainPanel = document.getElementById('uploadProfilePicMain') as HTMLDivElement;
    this.errorPanel = document.getElementById('uploadProfilePicError') as HTMLDivElement;
  }

  upload(): void {


    const formData: FormData = new FormData();
    formData.append('uploadedImage', this.image);

    const data = {
      token: UserTokenHandling.getUserToken(),
      user_id: UserTokenHandling.getUserId()
    };

    formData.append('uploadData', JSON.stringify(data));

    this.mainPanel.style.display = 'none';
    this.waitPanel.style.display = 'grid';
    
    
    fetch((projectConfig.api_url + 'upload_profile_pic'), {
      method: 'POST',
      body: formData
    }
    )
      .then(response => response.json())
      .then(json => {
        if (json.status === 'OK')
        {
          this.waitPanel.style.display = 'none';
          this.donePanel.style.display = 'grid';
        }
        else if (json.status.includes('error'))
        {
          this.waitPanel.style.display = 'none';
          this.errorPanel.style.display = 'grid';
        }
      });
      

  }

  previewImage(): void {
    const selectedFile = document.getElementById('fileToUpload') as HTMLInputElement;
    //@ts-ignore
    this.image = selectedFile.files[0];
    const imagePreview = document.getElementById('previewImage') as HTMLImageElement;
    imagePreview.src = URL.createObjectURL(this.image);
  }

}
