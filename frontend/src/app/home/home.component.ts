import { Component, OnInit } from '@angular/core';
import {UploadDialogComponent} from '../upload-dialog/upload-dialog.component';
import {MatDialog} from '@angular/material';
import {HttpClient} from '@angular/common/http';
import {LocalStorageService} from '../local-storage.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  public loginUser: string;
  public reposList: any;
  constructor(public dialog: MatDialog, public http: HttpClient, public localStorage: LocalStorageService, public router: Router) { }

  ngOnInit() {
    this.loginUser = this.localStorage.getUserEmail();
    if ( this.loginUser === undefined ) {
      this.router.navigate(['/login']);
    }
  }

  public openUploadDialog() {

    this.http.get('http://127.0.0.1:5000/upload?username=' + this.loginUser, {responseType: 'text'}).subscribe(data => {
      console.log(data);
      this.http.get('http://127.0.0.1:5000/list?username=' + this.loginUser).subscribe(res => {
        this.reposList = res;
      });

    });
  }
}
