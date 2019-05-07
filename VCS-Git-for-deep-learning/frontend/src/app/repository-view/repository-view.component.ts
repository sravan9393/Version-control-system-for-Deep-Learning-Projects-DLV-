import { Component, OnInit } from '@angular/core';
import {LocalStorageService} from '../local-storage.service';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-repository-view',
  templateUrl: './repository-view.component.html',
  styleUrls: ['./repository-view.component.css']
})
export class RepositoryViewComponent implements OnInit {

  public item: any;
  public loginUser: any;
  public repository: any;
  public changed: boolean;
  public commitFormGroup: FormGroup;
  constructor(public http: HttpClient, public localStorage: LocalStorageService, public router: Router, public fb: FormBuilder) { }

  ngOnInit() {
    this.commitFormGroup = this.fb.group({
      message: ['', [Validators.required, Validators.minLength(6)]]
    });

    this.item = this.localStorage.getItem();
    this.repository = this.item.key;

    this.loginUser = this.localStorage.getUserEmail();
    if ( this.loginUser === undefined ) {
      this.router.navigate(['/login']);
    }

  }

  public doCommit() {

    this.changed = false;
    if ( this.commitFormGroup.valid && this.commitFormGroup.dirty) {
      // console.log(this.commitFormGroup.get('message').value);
      this.http.get('http://127.0.0.1:5000/commit?username=' + this.loginUser + '&repository=' + this.repository + '&message=' + this.commitFormGroup.get('message').value, {responseType: 'text'}).subscribe(data => {
        console.log(data);
        this.changed = true;
      });

    }
  }

  public openUploadDialog() {

    this.http.get('http://127.0.0.1:5000/upload?username=' + this.loginUser, {responseType: 'text'}).subscribe(data => {
      console.log(data);
    });
  }
}
