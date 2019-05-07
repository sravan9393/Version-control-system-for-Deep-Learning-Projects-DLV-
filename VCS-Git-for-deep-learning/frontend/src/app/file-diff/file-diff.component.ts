import {Component, Input, OnChanges, OnInit, SimpleChange, SimpleChanges} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {LocalStorageService} from '../local-storage.service';
import { ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-file-diff',
  templateUrl: './file-diff.component.html',
  styleUrls: ['./file-diff.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class FileDiffComponent implements OnInit, OnChanges {

  public outputHtml: any;
  @Input() fileDiff: any;
  @Input() repository: any;
  @Input() changed: any;
  public username: any;
  @Input() version: any;

  constructor(public http: HttpClient, public localStorage: LocalStorageService) { }

  ngOnInit() {

    this.outputHtml = '<div><br><br><br>Click on any file to view changes<br><br><br></div>'
    this.username = this.localStorage.getUserEmail();

    this.version = 'None';
  }

  ngOnChanges(changes: SimpleChanges) {

    if (this.changed) {
      this.outputHtml = '<div>No Changes to view</div>';
      this.changed = '';
    }

      // console.log(this.fileDiff);
    if (this.fileDiff !== undefined) {

      if ( this.version !== 'None') {
        this.http.get('http://127.0.0.1:5000/historyfilediff?username=' + this.username + '&repository=' + this.repository + '&filename=' + this.fileDiff + '&versions=' + this.version,
          {responseType: 'text'})
          .subscribe(data => {
            console.log(data);
            this.outputHtml = data;
          });
      } else {
        this.http.get('http://127.0.0.1:5000/filediff?username=' + this.username + '&repository=' + this.repository + '&filename=' + this.fileDiff,
          {responseType: 'text'})
          .subscribe(data => {
            // console.log(data);
            this.outputHtml = data;
          });
      }
    }
  }

}
