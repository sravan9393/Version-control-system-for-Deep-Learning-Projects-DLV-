import {Component, Input, OnInit, Injectable, OnChanges, SimpleChanges} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {LocalStorageService} from '../local-storage.service';
import {CollectionViewer, SelectionChange} from '@angular/cdk/collections';
import {FlatTreeControl} from '@angular/cdk/tree';
import {BehaviorSubject, merge, Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {NestedTreeControl} from '@angular/cdk/tree';
import {MatTreeNestedDataSource} from '@angular/material/tree';

/*
interface FoodNode {
  name: string;
  children?: FoodNode[];
}
*/
@Component({
  selector: 'app-repo-changes',
  templateUrl: './repo-changes.component.html',
  styleUrls: ['./repo-changes.component.css']
})
export class RepoChangesComponent implements OnInit, OnChanges {

  public filesStatus: any;
  public loginUser: any;
  @Input() repository: any;
  public interval: any;
  public outputHtml: any;
  @Input() changed: boolean;

  public version: any;

  public fileDiff: any;
  public TREE_DATA: any;
  treeControl = new NestedTreeControl<any>(node => node.children);
  dataSource = new MatTreeNestedDataSource<any>();

  hasChild = (_: number, node: any) => !!node.children && node.children.length > 0;

  constructor(public http: HttpClient, public router: Router, public localStorage: LocalStorageService) {
    this.dataSource.data = this.TREE_DATA;
  }

  ngOnInit() {
    this.outputHtml = '<div></div>';
    // console.log(this.outputHtml);

    this.loginUser = this.localStorage.getUserEmail();
    if (this.loginUser === undefined) {
      this.router.navigate(['/login']);
    }

    const item = this.localStorage.getItem();
    this.repository = item.key;

    this.http.get('http://127.0.0.1:5000/status?username=' + this.loginUser + '&repository=' + this.repository).subscribe(data => {
      console.log(data);
      this.filesStatus = data;
      this.TREE_DATA = data;
      this.dataSource.data = this.TREE_DATA;
    });

    this.interval = setInterval(() => {
      this.yourservicecallmethod();
    }, 1 * 30 * 1000);
  }


  ngOnChanges(changes: SimpleChanges): void {

    if ( this.changed) {
      this.yourservicecallmethod();
    }
  }

  yourservicecallmethod() {
    this.http.get('http://127.0.0.1:5000/status?username=' + this.loginUser + '&repository=' + this.repository).subscribe(data => {
      console.log(data);
      this.filesStatus = data;
      this.TREE_DATA = data;
      this.dataSource.data = this.TREE_DATA;
    });
  }

  getDiff(fileName) {
    // console.log(fileName);
    this.fileDiff = fileName.path;
    this.version = 'None';
  }
}
