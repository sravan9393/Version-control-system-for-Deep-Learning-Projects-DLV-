import { Component, OnInit } from '@angular/core';
import {UploadDialogComponent} from '../upload-dialog/upload-dialog.component';
import {MatDialog} from '@angular/material';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(public dialog: MatDialog) { }

  ngOnInit() {
  }

  public openUploadDialog() {
    const dialogRef = this.dialog.open(UploadDialogComponent, { width: '50%', height: '50%' });
  }

}
