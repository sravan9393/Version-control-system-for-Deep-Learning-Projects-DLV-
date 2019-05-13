import {Component, Input, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {LocalStorageService} from '../local-storage.service';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {NestedTreeControl} from '@angular/cdk/tree';
import {MatTreeNestedDataSource} from '@angular/material';

/*
interface FoodNode {
  name: string;
  children?: FoodNode[];
}

 public TREE_DATA: FoodNode[];
  treeControl = new NestedTreeControl<FoodNode>(node => node.children);
  dataSource = new MatTreeNestedDataSource<FoodNode>();

  hasChild = (_: number, node: FoodNode) => !!node.children && node.children.length > 0;

*/
@Component({
  selector: 'app-repo-code',
  templateUrl: './repo-code.component.html',
  styleUrls: ['./repo-code.component.css']
})
export class RepoCodeComponent implements OnInit, OnChanges {

  public loginUser: any;
  public item: any;
  public repository: any;
  @Input() changed: any;

  public TREE_DATA: any;
  treeControl = new NestedTreeControl<any>(node => node.children);
  dataSource = new MatTreeNestedDataSource<any>();

  hasChild = (_: number, node: any) => !!node.children && node.children.length > 0;

  constructor(public localStorage: LocalStorageService, public http: HttpClient, public router: Router) {
    this.dataSource.data = this.TREE_DATA;
    }


  ngOnInit() {

    this.loginUser = this.localStorage.getUserEmail();
    if (this.loginUser === undefined) {
      this.router.navigate(['/login']);
    }

    this.item = this.localStorage.getItem();
    this.repository = this.item.key;
    console.log(this.item);

    this.http.get('http://127.0.0.1:5000/listoffiles?username=' + this.loginUser + '&repository=' + this.repository).subscribe(data => {
        // console.log(data);
        this.TREE_DATA = data;
        this.dataSource.data = this.TREE_DATA;
      });

  }

  ngOnChanges(changes: SimpleChanges): void {

    if (!this.changed) {
      return;
    }
    // console.log(this.changed);
    this.loginUser = this.localStorage.getUserEmail();
    if (this.loginUser === undefined) {
      this.router.navigate(['/login']);
    }


    this.http.get('http://127.0.0.1:5000/list?username=' + this.loginUser).subscribe(data => {
      for ( const key in data ) {
        if ( key === this.repository ) {
          const pair = {key: '', value: {}};
          pair.key = key;
          pair.value = data[key];
          this.item = pair;
        }
      }

      this.repository = this.item.key;
      this.localStorage.setItem(this.item);
      console.log(this.item);
    });

    this.item = this.localStorage.getItem();
    this.repository = this.item.key;
    console.log(this.item);

    this.http.get('http://127.0.0.1:5000/listoffiles?username=' + this.loginUser + '&repository=' + this.repository).subscribe(data => {
      // console.log(data);
      this.TREE_DATA = data;
      this.dataSource.data = this.TREE_DATA;
    });
  }


}
