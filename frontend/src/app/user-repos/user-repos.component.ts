import {Component, Input, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {LocalStorageService} from '../local-storage.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-user-repos',
  templateUrl: './user-repos.component.html',
  styleUrls: ['./user-repos.component.css']
})
export class UserReposComponent implements OnInit {

  @Input() reposList: any;
  public loginUser: string;
  public item: any;

  constructor(public http: HttpClient, public localStorage: LocalStorageService, public router: Router) {
  }

  ngOnInit() {
    this.loginUser = this.localStorage.getUserEmail();
    if (this.loginUser === undefined) {
      this.router.navigate(['/login']);
    }

    this.http.get('http://127.0.0.1:5000/list?username=' + this.loginUser).subscribe(data => {
      this.reposList = data;
    });
  }

  navigate(item) {
    this.localStorage.setItem(item);
    this.router.navigate(['/repositoryView']);
  }
}
