import {Component, Input, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {NestedTreeControl} from '@angular/cdk/tree';
import {MatTreeNestedDataSource} from '@angular/material';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {LocalStorageService} from '../local-storage.service';


interface FoodNode {
  name: string;
  children?: FoodNode[];
}

@Component({
  selector: 'app-repo-history',
  templateUrl: './repo-history.component.html',
  styleUrls: ['./repo-history.component.css']
})
export class RepoHistoryComponent implements OnInit, OnChanges {

  public loginUser: any;
  @Input() repository: any;
  public interval: any;
  public outputHtml: any;
  @Input() changed: boolean;
  public commits: any;
  public version: any;
  public commit: any;

  public fileDiff: any;
  public TREE_DATA: FoodNode[];
  treeControl = new NestedTreeControl<FoodNode>(node => node.children);
  dataSource = new MatTreeNestedDataSource<FoodNode>();

  hasChild = (_: number, node: FoodNode) => !!node.children && node.children.length > 0;

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

    this.getCommitHistory();
  }


  ngOnChanges(changes: SimpleChanges): void {

    if (this.changed) {
      this.getCommitHistory();
    }
  }

  getCommitHistory() {
    this.http.get('http://127.0.0.1:5000/history?username=' + this.loginUser + '&repository=' + this.repository).subscribe(data => {
      console.log(data);

      this.commits = data;

      const pair = {key: '', value: {}};
      pair.key = 'commit.1';
      pair.value = data[pair.key];
      this.commit = pair;

      this.TREE_DATA = data['commit.1'].changed_files;
      this.dataSource.data = this.TREE_DATA;
      console.log(this.dataSource.data);
    });
  }

  getDiff(fileName) {
    // console.log(fileName);
    this.fileDiff = fileName.path;
    const key = this.commit.key;
    const version1 = parseInt(key.split('.')[1], 10);
    const nextVersion = 'commit.' + (version1 - 1);

    if ( nextVersion in this.commits) {
      this.version = version1 + ' ' + (version1 - 1);
    } else {
      this.version = '' + version1;
    }

  }

  getChangedFiles(commit) {
    this.TREE_DATA = commit.value.changed_files;
    this.dataSource.data = this.TREE_DATA;
    this.commit = commit;
  }

}
